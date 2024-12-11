const { expect } = require("chai");
const { ethers, deployments } = require("hardhat");
const fs = require('fs-extra');
const path = require('path');

const { ZeroAddress } = ethers;

describe("Deploy Script", function () {
    let deployer, validator1, validator2, validator3;
    const deployPath = path.join('./deployments/localhost');
    const backupPath = path.join('./copy_deployments/localhost');

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

    before(async function () {
        await deployments.fixture(['GhostContract']);
        [deployer, validator1, validator2, validator3] = await ethers.getSigners();
    });

    describe("Deployment Files Verification", function() {
        it("should have all contracts in both deployment and backup directories", async function() {
            console.log("\n[Test] Verifying contract files in both directories...");

            for (const contractName of expectedContracts) {
                // Verify in deployments
                const deployContractPath = path.join(deployPath, `${contractName}.json`);
                expect(
                    await fs.pathExists(deployContractPath),
                    `${contractName} should exist in deployments directory`
                ).to.be.true;

                // Verify in backup
                const backupContractPath = path.join(backupPath, `${contractName}.json`);
                expect(
                    await fs.pathExists(backupContractPath),
                    `${contractName} should exist in backup directory`
                ).to.be.true;

                // Verify that the files are valid and match
                const deployData = JSON.parse(await fs.readFile(deployContractPath, 'utf8'));
                const backupData = JSON.parse(await fs.readFile(backupContractPath, 'utf8'));

                expect(deployData.address, `${contractName} should have valid address in deployments`)
                    .to.match(/^0x[a-fA-F0-9]{40}$/);
                expect(backupData.address, `${contractName} should have valid address in backup`)
                    .to.match(/^0x[a-fA-F0-9]{40}$/);
                expect(deployData.address, `${contractName} should have same address in both directories`)
                    .to.equal(backupData.address);

                console.log(`[Test] ✓ ${contractName} verified in both directories`);
            }
        });
    });

    // We need to add more tests to verify the contract connections and configurations
});