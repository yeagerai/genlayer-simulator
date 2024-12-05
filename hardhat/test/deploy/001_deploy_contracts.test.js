const { expect } = require("chai");
const { ethers, deployments } = require("hardhat");
const fs = require('fs');
const path = require('path');

describe("Deploy Script", function () {
  let deployer;
  const deploymentDir = path.join('./deployments/hardhat');

  // Setup before all tests
  before(async function () {
    // Create deployment directory and .chainId file
    fs.mkdirSync(deploymentDir, { recursive: true });
    fs.writeFileSync(path.join(deploymentDir, '.chainId'), '31337');
  });

  // Cleanup after all tests
  after(async function () {
    // Remove test deployment directory
    if (fs.existsSync(deploymentDir)) {
      fs.rmSync(deploymentDir, { recursive: true, force: true });
    }
  });

  beforeEach(async function () {
    [deployer] = await ethers.getSigners();
  });

  it("should deploy GhostContract successfully", async function () {
    await deployments.fixture(["GhostContract"]);
    const deploymentData = await deployments.get("GhostContract");
    const GhostContract = await ethers.getContractAt("GhostContract", deploymentData.address);

    expect(await GhostContract.getAddress()).to.be.properAddress;
  });

  it("should create deployment file with correct data", async function () {
    await deployments.fixture(["GhostContract"]);
    const deploymentData = await deployments.get("GhostContract");
    const GhostContract = await ethers.getContractAt("GhostContract", deploymentData.address);

    const deploymentPath = path.join(deploymentDir, 'GhostContract.json');
    const savedDeploymentData = JSON.parse(fs.readFileSync(deploymentPath, 'utf8'));

    expect(savedDeploymentData.address).to.equal(await GhostContract.getAddress());
    expect(savedDeploymentData.abi).to.not.be.empty;
    expect(savedDeploymentData.bytecode).to.not.be.empty;
    expect(savedDeploymentData.transactionHash).to.match(/^0x[a-fA-F0-9]{64}$/);
  });

  it("should use correct deployment parameters", async function () {
    const deployResult = await deployments.deploy('GhostContract', {
      from: deployer.address,
      args: [],
      log: true,
      deterministicDeployment: false,
      gasPrice: 0,
      gasLimit: 5000000,
      waitConfirmations: 1
    });

    expect(deployResult.address).to.be.properAddress;
  });
});