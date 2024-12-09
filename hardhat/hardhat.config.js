require("@nomicfoundation/hardhat-toolbox");
require("hardhat-deploy");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      },
      viaIR: true
    }
  },
  networks: {
    hardhat: {
      mining: {
        auto: true,
        interval: 0
      },
      chainId: 31337,
      gasPrice: 0,
      initialBaseFeePerGas: 0,
      blockGasLimit: 30000000,
      live: false,
      saveDeployments: true,
      allowUnlimitedContractSize: true,
      tags: ['local']
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
    deploy: "./deploy",
    deployments: "./deployments"
  },
  namedAccounts: {
    deployer: {
      default: 0
    }
  }
};