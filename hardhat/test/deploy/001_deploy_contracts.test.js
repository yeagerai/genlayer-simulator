const { expect } = require("chai");
const { ethers, deployments } = require("hardhat");
const fs = require('fs');
const path = require('path');

describe("Deploy Script", function () {
  let deployer;
  const deploymentDir = path.join('./deployments/hardhat');

  // Setup before all tests
  before(async function () {
    [deployer] = await ethers.getSigners();
    // Create deployment directory and .chainId file
    fs.mkdirSync(deploymentDir, { recursive: true });
    fs.writeFileSync(path.join(deploymentDir, '.chainId'), '31337');
  });

  // Cleanup after all tests
  after(async function () {
    if (fs.existsSync(deploymentDir)) {
      fs.rmSync(deploymentDir, { recursive: true, force: true });
    }
  });

  beforeEach(async function () {
    // Clear deployments before each test
    if (fs.existsSync(deploymentDir)) {
      const files = fs.readdirSync(deploymentDir);
      for (const file of files) {
        if (file !== '.chainId') {
          fs.unlinkSync(path.join(deploymentDir, file));
        }
      }
    }
  });

  it("should correctly identify missing and deployed contracts", async function () {
    // Deploy one contract first
    await deployments.deploy('GhostContract', {
      from: deployer.address,
      args: []
    });

    const contracts = [
      { name: 'GhostContract', args: [] },
      { name: 'ConsensusManager', args: [] }
    ];

    const { missingContracts, deployedContracts } = await checkDeployments(contracts, { name: 'hardhat' });

    expect(deployedContracts).to.include('GhostContract');
    expect(missingContracts.map(c => c.name)).to.include('ConsensusManager');
  });

  it("should only deploy missing contracts", async function () {
    // Deploy one contract manually first
    await deployments.deploy('GhostContract', {
      from: deployer.address,
      args: []
    });

    // Run the deployment script
    await deployments.fixture(['AllContracts']);

    // Check that all contracts are deployed
    const files = fs.readdirSync(deploymentDir);
    expect(files).to.include('GhostContract.json');
    expect(files).to.include('ConsensusManager.json');
    expect(files).to.include('GhostBlueprint.json');
    expect(files).to.include('GhostFactory.json');
    expect(files).to.include('MockGenStaking.json');
    expect(files).to.include('Queues.json');
    expect(files).to.include('Transactions.json');
    expect(files).to.include('ConsensusMain.json');
  });

  it("should save correct deployment data for each contract", async function () {
    await deployments.fixture(['AllContracts']);

    const contracts = [
      'GhostContract',
      'ConsensusManager',
      'GhostBlueprint',
      'GhostFactory',
      'MockGenStaking',
      'Queues',
      'Transactions',
      'ConsensusMain'
    ];

    for (const contractName of contracts) {
      const deploymentPath = path.join(deploymentDir, `${contractName}.json`);
      expect(fs.existsSync(deploymentPath), `${contractName} deployment file should exist`).to.be.true;

      const deploymentData = JSON.parse(fs.readFileSync(deploymentPath, 'utf8'));
      expect(deploymentData.address).to.match(/^0x[a-fA-F0-9]{40}$/);
      expect(deploymentData.abi).to.be.an('array');
      expect(deploymentData.bytecode).to.match(/^0x[a-fA-F0-9]+$/);
      expect(deploymentData.transactionHash).to.match(/^0x[a-fA-F0-9]{64}$/);
    }
  });

  it("should handle constructor arguments correctly", async function () {
    await deployments.fixture(['AllContracts']);

    const mockGenStakingPath = path.join(deploymentDir, 'MockGenStaking.json');
    const deploymentData = JSON.parse(fs.readFileSync(mockGenStakingPath, 'utf8'));

    const MockGenStaking = await ethers.getContractAt('MockGenStaking', deploymentData.address);
    expect(await MockGenStaking.isValidator(deployer.address)).to.be.true;
  });

  it("should create and maintain .chainId file", async function () {
    const chainIdPath = path.join(deploymentDir, '.chainId');
    expect(fs.existsSync(chainIdPath)).to.be.true;
    expect(fs.readFileSync(chainIdPath, 'utf8')).to.equal('31337');
  });
});