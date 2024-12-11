const { expect } = require("chai");
const { ethers } = require("hardhat");
const { deployments } = require("hardhat");
const fs = require('fs');
const path = require('path');

// Define the AddressZero constant
const { ZeroAddress } = ethers;

describe("Deploy Script", function () {
    let deployer, validator1, validator2, validator3;
    const deploymentDir = path.join('./deployments/localhost');
    const expectedContracts = [
        'GhostContract',
        'ConsensusManager',
        'GhostBlueprint',
        'GhostFactory',
        'MockGenStaking',
        'Queues',
        'Transactions',
        'ConsensusMain'
    ];

    // Deploy all contracts before tests
    before(async function () {
        // Reset deployments to ensure clean state
        await deployments.fixture(['GhostContract']);

        [deployer, validator1, validator2, validator3] = await ethers.getSigners();
        console.log("\n=== Starting Contract Verification ===");

        // Verificar que todos los contratos estén desplegados
        console.log("\n[Test] Verifying all contracts are deployed...");
        for (const contractName of expectedContracts) {
            const deployment = await deployments.get(contractName).catch(() => null);
            if (!deployment) {
                throw new Error(`Required contract ${contractName} is not deployed!`);
            }
            console.log(`[Test] ✓ ${contractName} deployment verified`);
        }
    });

    describe("Contract Deployment Data", function() {
        it("should have valid deployment data for all contracts", async function () {
            for (const contractName of expectedContracts) {
                const deployment = await deployments.get(contractName);

                expect(deployment).to.have.property('address').that.matches(/^0x[a-fA-F0-9]{40}$/);
                expect(deployment).to.have.property('abi').that.is.an('array').that.is.not.empty;
                expect(deployment).to.have.property('transactionHash').that.matches(/^0x[a-fA-F0-9]{64}$/);
                expect(deployment).to.have.property('bytecode').that.matches(/^0x[a-fA-F0-9]+$/);

                console.log(`[Test] ✓ ${contractName} deployment data is valid`);
            }
        });
    });

    describe("Contract Initialization and Connections", function() {
        it("should have GhostFactory properly initialized with blueprint", async function() {
            console.log("\n[Test] Verifying GhostFactory initialization...");
            const deployment = await deployments.get('GhostFactory');
            const ghostFactory = await ethers.getContractAt('GhostFactory', deployment.address);

            const blueprintAddress = await ghostFactory.ghostBlueprint();
            expect(blueprintAddress).to.not.equal(ZeroAddress, "GhostFactory blueprint not set");
            console.log("[Test] ✓ GhostFactory blueprint is properly set");
        });

        it("should have ConsensusMain properly connected to all contracts", async function() {
            console.log("\n[Test] Verifying ConsensusMain connections...");
            const deployment = await deployments.get('ConsensusMain');
            const consensusMain = await ethers.getContractAt('ConsensusMain', deployment.address);

            const ghostFactoryAddress = await consensusMain.ghostFactory();
            const genStakingAddress = await consensusMain.genStaking();
            const genQueueAddress = await consensusMain.genQueue();
            const genTransactionsAddress = await consensusMain.genTransactions();

            expect(ghostFactoryAddress).to.not.equal(ZeroAddress, "GhostFactory connection not set");
            expect(genStakingAddress).to.not.equal(ZeroAddress, "GenStaking connection not set");
            expect(genQueueAddress).to.not.equal(ZeroAddress, "GenQueue connection not set");
            expect(genTransactionsAddress).to.not.equal(ZeroAddress, "GenTransactions connection not set");

            console.log("[Test] ✓ ConsensusMain connections are properly set");
        });

        it("should have validators properly set up in MockGenStaking", async function() {
            console.log("\n[Test] Verifying validator setup...");
            const deployment = await deployments.get('MockGenStaking');
            const mockGenStaking = await ethers.getContractAt('MockGenStaking', deployment.address);

            expect(await mockGenStaking.isValidator(validator1.address)).to.be.true, "Validator1 not set";
            expect(await mockGenStaking.isValidator(validator2.address)).to.be.true, "Validator2 not set";
            expect(await mockGenStaking.isValidator(validator3.address)).to.be.true, "Validator3 not set";

            console.log("[Test] ✓ Validators are properly set up");
        });
    });
});