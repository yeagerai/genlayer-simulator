#!/bin/sh

echo "Checking and compiling contracts if needed..."
npx hardhat compile

echo "Starting Hardhat node..."
npx hardhat node --hostname 0.0.0.0 --no-deploy &

# Wait for the node to start
sleep 5

# Check if the contract is already deployed (using hardhat network)
if [ ! -f "/app/deployments/hardhat/GhostContract.json" ]; then
    echo "Running deployments..."
    npx hardhat deploy
else
    echo "Contracts already deployed, skipping deployment..."
fi

# Keep the container running
wait