module.exports = async function ({ getNamedAccounts, deployments, network }) {
    const { deploy, save, getArtifact } = deployments;
    const { deployer } = await getNamedAccounts();

    console.log("Starting deployment of GhostContract...");

    const result = await deploy('GhostContract', {
      from: deployer,
      args: [],
      log: true,
      deterministicDeployment: false,
      gasPrice: 0,
      gasLimit: 5000000,
      waitConfirmations: 1
    });

    const artifact = await getArtifact('GhostContract');
    const deploymentData = {
      address: result.address,
      abi: artifact.abi,
      bytecode: artifact.bytecode,
      transactionHash: result.transactionHash
    };

    const fs = require('fs');
    const path = require('path');
    const deploymentDir = path.join('./deployments', network.name);
    const deploymentFile = path.join(deploymentDir, 'GhostContract.json');

    fs.mkdirSync(deploymentDir, { recursive: true });

    fs.writeFileSync(deploymentFile, JSON.stringify(deploymentData, null, 2));

    console.log(`Deployment successful! Contract deployed at: ${result.address}`);
  };

  module.exports.tags = ['GhostContract'];