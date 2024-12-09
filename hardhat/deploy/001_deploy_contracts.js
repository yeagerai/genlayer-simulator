// Import required modules
const { ethers } = require("hardhat");
const fs = require('fs');
const path = require('path');

/**
 * Ensures deployment directory exists and contains proper chain ID file
 * @param {Object} network - Network configuration object
 */
async function ensureDeploymentDir(network) {
    const deploymentDir = path.join('./deployments', network.name);
    fs.mkdirSync(deploymentDir, { recursive: true });

    // Create .chainId file if it doesn't exist
    const chainIdPath = path.join(deploymentDir, '.chainId');
    if (!fs.existsSync(chainIdPath)) {
        // For hardhat network, chainId is 31337
        const chainId = network.name === 'hardhat' ? '31337' : network.config.chainId.toString();
        fs.writeFileSync(chainIdPath, chainId);
        console.log(`Created .chainId file with chainId: ${chainId}`);
    }
}

/**
 * Checks which contracts need deployment by comparing against existing deployments
 * @param {Array} contracts - Array of contract configurations to check
 * @param {Object} network - Network configuration object
 * @returns {Object} Object containing arrays of missing and deployed contracts
 */
async function checkDeployments(contracts, network) {
    const deploymentDir = path.join('./deployments', network.name);
    let missingContracts = [];
    let deployedContracts = [];

    // Check each contract's deployment status
    for (const contract of contracts) {
        const deploymentFile = path.join(deploymentDir, `${contract.name}.json`);
        if (!fs.existsSync(deploymentFile)) {
            missingContracts.push(contract);
        } else {
            deployedContracts.push(contract.name);
        }
    }

    // Log deployment status
    if (deployedContracts.length > 0) {
        console.log("Already deployed contracts:", deployedContracts.join(", "));
    }
    if (missingContracts.length > 0) {
        console.log("Missing contracts:", missingContracts.map(c => c.name).join(", "));
    }

    return { missingContracts, deployedContracts };
}

/**
 * Deploys a contract and saves its deployment information
 * @param {Object} contractConfig - Configuration for the contract to deploy
 * @param {string} deployer - Address of the deploying account
 * @param {Object} deployments - Hardhat deployments object
 * @param {Object} network - Network configuration object
 * @returns {Object} Deployment result object
 */
async function deployAndSave(contractConfig, deployer, deployments, network) {
    const { deploy, getArtifact } = deployments;
    const { name, args = [] } = contractConfig;

    console.log(`\nDeploying ${name}...`);

    // Deploy the contract
    const deploymentResult = await deploy(name, {
        from: deployer,
        args: typeof args === 'function' ? args(deployer) : args,
        log: true,
        deterministicDeployment: false,
        gasPrice: 0,
        gasLimit: 5000000,
        waitConfirmations: 1
    });

    // Prepare deployment data for saving
    const artifact = await getArtifact(name);
    const deploymentData = {
        address: deploymentResult.address,
        abi: artifact.abi,
        bytecode: artifact.bytecode,
        transactionHash: deploymentResult.transactionHash
    };

    // Save deployment data to file
    const deploymentDir = path.join('./deployments', network.name);
    const deploymentFile = path.join(deploymentDir, `${name}.json`);

    fs.mkdirSync(deploymentDir, { recursive: true });
    fs.writeFileSync(deploymentFile, JSON.stringify(deploymentData, null, 2));

    console.log(`${name} deployed at: ${deploymentResult.address}`);
    return deploymentResult;
}

/**
 * Main deployment script
 * Handles the deployment of all contracts in the system
 */
module.exports = async function ({ getNamedAccounts, deployments, network }) {
    const { deployer } = await getNamedAccounts();

    // Ensure deployment directory exists and has chain ID file
    await ensureDeploymentDir(network);

    // Define all contracts to be deployed
    const contracts = [
        {
            name: 'GhostBlueprint',
            args: []
        },
        {
            name: 'GhostContract',
            args: []
        },
        {
            name: 'ConsensusManager',
            args: []
        },
        {
            name: 'GhostFactory',
            args: []
        },
        {
            name: 'MockGenStaking',
            args: (deployer) => [deployer]
        },
        {
            name: 'Queues',
            args: []
        },
        {
            name: 'Transactions',
            args: []
        },
        {
            name: 'ConsensusMain',
            args: []
        }
    ];

    // Check which contracts need deployment
    const { missingContracts, deployedContracts } = await checkDeployments(contracts, network);

    if (missingContracts.length === 0) {
        console.log("\nAll contracts are already deployed!");
        return;
    }

    console.log("\nStarting deployment of missing contracts...");

    // Deploy missing contracts and track results
    const newlyDeployedContracts = {};
    for (const contract of missingContracts) {
        const deployment = await deployAndSave(contract, deployer, deployments, network);
        newlyDeployedContracts[contract.name] = deployment;
    }

    // Initialize contracts if any were newly deployed
    if (Object.keys(newlyDeployedContracts).length > 0) {
        await initializeContracts(newlyDeployedContracts, deployer);
    }

    // Log newly deployed contracts
    if (Object.keys(newlyDeployedContracts).length > 0) {
        console.log("\nNewly deployed contracts:");
        for (const [name, deployment] of Object.entries(newlyDeployedContracts)) {
            console.log(`${name}: ${deployment.address}`);
        }
    }

    console.log("\nDeployment complete!");
};

// Add deployment tags for selective deployment
module.exports.tags = ['AllContracts'];