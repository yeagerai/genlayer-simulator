// Import required modules
const { ethers } = require("hardhat");
const fs = require('fs-extra');
const path = require('path');
const { ZeroAddress } = ethers;

/**
 * Ensures deployment directory exists and contains proper chain ID file
 * @param {Object} hre - Hardhat runtime environment
 * @param {string|number} chainId - Current chain ID
 */
async function ensureDeploymentDir(hre, chainId) {
    const networkName = hre.network.name; // e.g. 'hardhat' or 'localhost'
    const deploymentDir = path.join('./deployments', networkName);
    fs.mkdirSync(deploymentDir, { recursive: true });

    // Create the .chainId file if it doesn't exist
    const chainIdPath = path.join(deploymentDir, '.chainId');
    if (!fs.existsSync(chainIdPath)) {
        fs.writeFileSync(chainIdPath, chainId.toString());
        console.log(`Created .chainId file with chainId: ${chainId}`);
    }
}

/**
 * Checks which contracts need deployment by comparing against existing backups
 * @param {Array} contracts - Array of contract configs to check
 * @param {Object} hre - Hardhat runtime environment
 * @returns {Object} { missingContracts, deployedContracts }
 */
async function checkDeployments(contracts, hre) {
    const backupPath = path.join('./copy_deployments/localhost');
    const deployPath = path.join('./deployments/localhost');
    let missingContracts = [];
    let deployedContracts = [];

    // Check if the backup directory exists
    if (!fs.existsSync(backupPath)) {
        console.log("\nNo backup directory found. Will proceed with fresh deployment.");
        return { missingContracts: contracts, deployedContracts: [] };
    }

    // Check each contract in the backup
    for (const contract of contracts) {
        const contractPath = path.join(backupPath, `${contract.name}.json`);

        if (!fs.existsSync(contractPath)) {
            missingContracts.push(contract);
            continue;
        }

        try {
            const contractData = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
            if (!contractData.address) {
                missingContracts.push(contract);
            } else {
                deployedContracts.push(contract.name);
            }
        } catch (error) {
            console.log(`Error reading backup for ${contract.name}:`, error);
            missingContracts.push(contract);
        }
    }

    if (deployedContracts.length > 0) {
        console.log("\nAlready deployed contracts:", deployedContracts.join(", "));
    }
    if (missingContracts.length > 0) {
        console.log("\nMissing contracts:", missingContracts.map(c => c.name).join(", "));
    }

    return { missingContracts, deployedContracts };
}

module.exports = async function (hre) {
    const { getNamedAccounts, deployments, getChainId, network } = hre;
    const { deploy, execute, get, log } = deployments;
    const { deployer } = await getNamedAccounts();

    const chainId = await getChainId();
    await ensureDeploymentDir(hre, chainId);

    // Define required contracts
    const requiredContracts = [
        { name: 'GhostBlueprint', args: [] },
        { name: 'GhostContract', args: [] },
        { name: 'ConsensusManager', args: [] },
        { name: 'GhostFactory', args: [] },
        { name: 'MockGenStaking', args: (deployer) => [deployer] },
        { name: 'Queues', args: [] },
        { name: 'Transactions', args: [] },
        { name: 'ConsensusMain', args: [] }
    ];

    const { missingContracts, deployedContracts } = await checkDeployments(requiredContracts, hre);

    if (missingContracts.length > 0) {
        console.log("\nMissing contracts detected. Redeploying all contracts...");

        // Deploy all required contracts
        for (const contract of requiredContracts) {
            const args = typeof contract.args === 'function' ? contract.args(deployer) : contract.args;
            console.log(`\nDeploying ${contract.name}...`);
            await deploy(contract.name, {
                from: deployer,
                args,
                log: true,
                deterministicDeployment: false,
                gasPrice: 0,
                gasLimit: 5000000,
                waitConfirmations: 1
            });
        }

        // Retrieve deployed contract addresses
        const ghostContract = await get("GhostContract");
        const consensusManager = await get("ConsensusManager");
        const ghostFactory = await get("GhostFactory");
        const ghostBlueprint = await get("GhostBlueprint");
        const mockGenStaking = await get("MockGenStaking");
        const genQueue = await get("Queues");
        const genTransactions = await get("Transactions");
        const consensusMain = await get("ConsensusMain");

        // Get signers (validators)
        const signers = await ethers.getSigners();
        const [owner, validator1, validator2, validator3] = signers;

        console.log("\n=== Initializing Contracts ===");

        // Initialize GhostFactory
        log("\n[GhostFactory] Initializing...");
        await execute("GhostFactory", { from: deployer, log: true }, "initialize");
        await execute("GhostFactory", { from: deployer, log: true }, "setGhostBlueprint", ghostBlueprint.address);
        await execute("GhostFactory", { from: deployer, log: true }, "deployNewBeaconProxy");

        // Initialize ConsensusMain
        log("\n[ConsensusMain] Initializing...");
        await execute("ConsensusMain", { from: deployer, log: true }, "initialize", consensusManager.address);

        // Transactions & Queues initialization
        const consensusMainAddress = consensusMain.address;
        log("\n[GenTransactions/GenQueue] Initializing with ConsensusMain address...");
        await execute("Transactions", { from: deployer, log: true }, "initialize", consensusMainAddress);
        await execute("Queues", { from: deployer, log: true }, "initialize", consensusMainAddress);

        // Setup ConsensusMain connections
        log("\n[ConsensusMain] Setting contract connections...");
        await execute("ConsensusMain", { from: deployer, log: true }, "setGhostFactory", ghostFactory.address);
        await execute("ConsensusMain", { from: deployer, log: true }, "setGenStaking", mockGenStaking.address);
        await execute("ConsensusMain", { from: deployer, log: true }, "setGenQueue", genQueue.address);
        await execute("ConsensusMain", { from: deployer, log: true }, "setGenTransactions", genTransactions.address);

        // Configure GhostFactory and final settings
        log("\n[GhostFactory] Configuring final settings...");
        await execute("GhostFactory", { from: deployer, log: true }, "setGenConsensus", consensusMainAddress);
        await execute("GhostFactory", { from: deployer, log: true }, "setGhostManager", consensusMainAddress);
        await execute("Transactions", { from: deployer, log: true }, "setGenConsensus", consensusMainAddress);

        // Set Acceptance Timeout in ConsensusMain
        await execute("ConsensusMain", { from: deployer, log: true }, "setAcceptanceTimeout", 0);

        // Setup validators
        log("\n[MockGenStaking] Setting up validators...");
        await execute("MockGenStaking", { from: deployer, log: true }, "addValidators", [validator1.address, validator2.address, validator3.address]);

        console.log("\n=== Contract Initialization Complete ===");
        console.log("\nAll contracts have been deployed, initialized and updated in deployments!");
    } else {
        console.log("\nAll contracts are already deployed. No action needed.");

        try {
            const backupDir = path.join('./copy_deployments/localhost');
            const deployDir = path.join('./deployments/localhost');

            // Asegurar que el directorio de deployments existe
            await fs.ensureDir(deployDir);

            // Copiar desde el backup a deployments
            console.log("Restoring contracts from backup...");
            await fs.copy(backupDir, deployDir, { overwrite: true });
            console.log("Contracts restored from backup successfully.");

        } catch (error) {
            console.error("Error restoring contracts from backup:", error);
        }
    }
};