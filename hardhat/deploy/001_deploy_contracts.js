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
 * Initializes contracts and sets up connections
 * @param {Object} allContracts - Object containing all deployed contracts
 */
async function deployFixture(allContracts) {
    console.log("\nInitializing contracts and setting up connections...");
    const accounts = await ethers.getSigners();
    const [owner, validator1, validator2, validator3] = accounts;

    try {
        // Initialize GhostFactory first
        if (allContracts.GhostFactory && allContracts.GhostBlueprint) {
            console.log("Setting up GhostFactory...");
            const ghostFactory = await ethers.getContractAt('GhostFactory', allContracts.GhostFactory.address);
            await ghostFactory.initialize();
            await ghostFactory.setGhostBlueprint(allContracts.GhostBlueprint.address);
            await ghostFactory.deployNewBeaconProxy();
        }

        // Initialize ConsensusMain and its connections
        if (allContracts.ConsensusMain && allContracts.ConsensusManager) {
            console.log("Setting up ConsensusMain...");
            const consensusMain = await ethers.getContractAt('ConsensusMain', allContracts.ConsensusMain.address);
            await consensusMain.initialize(allContracts.ConsensusManager.address);

            // Initialize dependent contracts first
            if (allContracts.Transactions) {
                const transactions = await ethers.getContractAt('Transactions', allContracts.Transactions.address);
                await transactions.initialize(allContracts.ConsensusMain.address);
            }

            if (allContracts.Queues) {
                const queues = await ethers.getContractAt('Queues', allContracts.Queues.address);
                await queues.initialize(allContracts.ConsensusMain.address);
            }

            // Set up ConsensusMain connections
            if (allContracts.GhostFactory) {
                await consensusMain.setGhostFactory(allContracts.GhostFactory.address);
            }
            if (allContracts.MockGenStaking) {
                await consensusMain.setGenStaking(allContracts.MockGenStaking.address);
            }
            if (allContracts.Queues) {
                await consensusMain.setGenQueue(allContracts.Queues.address);
            }
            if (allContracts.Transactions) {
                await consensusMain.setGenTransactions(allContracts.Transactions.address);
            }
        }

        // Set up GhostFactory connections
        if (allContracts.GhostFactory && allContracts.ConsensusMain) {
            const ghostFactory = await ethers.getContractAt('GhostFactory', allContracts.GhostFactory.address);
            await ghostFactory.setGenConsensus(allContracts.ConsensusMain.address);
            await ghostFactory.setGhostManager(allContracts.ConsensusMain.address);
        }

        // Set up Transactions connections
        if (allContracts.Transactions && allContracts.ConsensusMain) {
            const transactions = await ethers.getContractAt('Transactions', allContracts.Transactions.address);
            await transactions.setGenConsensus(allContracts.ConsensusMain.address);
        }

        // Set acceptance timeout
        if (allContracts.ConsensusMain) {
            const consensusMain = await ethers.getContractAt('ConsensusMain', allContracts.ConsensusMain.address);
            await consensusMain.setAcceptanceTimeout(0);
        }

        // Setup validators
        if (allContracts.MockGenStaking) {
            console.log("Setting up validators...");
            const mockGenStaking = await ethers.getContractAt('MockGenStaking', allContracts.MockGenStaking.address);
            await mockGenStaking.addValidators([
                validator1.address,
                validator2.address,
                validator3.address
            ]);
        }

        console.log("Contract initialization and setup complete!");
    } catch (error) {
        console.error("Error in deployFixture:", error);
        throw error;
    }
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
    const allContracts = {};

    // Load the existing contracts
    for (const contractName of deployedContracts) {
        const deploymentFile = path.join('./deployments', network.name, `${contractName}.json`);
        const deploymentData = JSON.parse(fs.readFileSync(deploymentFile, 'utf8'));
        allContracts[contractName] = {
            address: deploymentData.address
        };
    }

    if (missingContracts.length > 0) {
        console.log("\nStarting deployment of missing contracts...");

        // Deploy missing contracts and track results
        for (const contract of missingContracts) {
            const deployment = await deployAndSave(contract, deployer, deployments, network);
            allContracts[contract.name] = deployment;
        }

        console.log("\nNewly deployed contracts:");
        for (const contract of missingContracts) {
            console.log(`${contract.name}: ${allContracts[contract.name].address}`);
        }
    } else {
        console.log("\nAll contracts are already deployed!");
        // return; // Comment this to call deployFixture even if all the contracts are already deployed
    }

    // Always run deployFixture with all contracts
    await deployFixture(allContracts);

};

// Add deployment tags for selective deployment
module.exports.tags = ['AllContracts'];