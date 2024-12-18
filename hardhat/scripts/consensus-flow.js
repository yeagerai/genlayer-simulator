const hre = require("hardhat");


async function generateSignature(signer, currentSeed) {
    const seedBytes = ethers.zeroPadValue(ethers.toBeHex(currentSeed), 32);
    const vrfProof = await signer.signMessage(ethers.getBytes(seedBytes));
    return vrfProof;
}

async function main() {
    console.log("Starting consensus flow...");

    // Get signers
    const [owner, validator1, validator2, validator3] = await hre.ethers.getSigners();
    const validators = [validator1, validator2, validator3];

    // Get contract instance
    const consensusMainAddress = require("../deployments/localhost/ConsensusMain.json").address;
    const consensusMain = await hre.ethers.getContractAt("ConsensusMain", consensusMainAddress);

    // 1. Add transaction
    console.log("\n1. Adding transaction...");
    const tx = await consensusMain.connect(owner).addTransaction(
        ethers.ZeroAddress,
        ethers.ZeroAddress,
        3,
        "0x"
    );
    const receipt = await tx.wait();

    // Find the NewTransaction event
    const newTxEvent = receipt.logs?.find(
        (log) => consensusMain.interface.parseLog(log)?.name === "NewTransaction"
    );
    if (!newTxEvent) throw new Error("NewTransaction event not found");

    const parsedLog = consensusMain.interface.parseLog(newTxEvent);
    const txId = parsedLog.args[0];
    const ghostAddress = parsedLog.args[1];
    const activatorAddress = parsedLog.args[2];

    console.log("- Transaction ID:", txId);
    console.log("- Ghost Address:", ghostAddress);
    console.log("- Activator:", activatorAddress);

    // 2. Activate transaction
    console.log("\n2. Activating transaction...");
    const activator = validators.find(v => v.address === activatorAddress);
    const currentSeed = await consensusMain.recipientRandomSeed(ghostAddress);
    const vrfProofActivate = await generateSignature(activator, BigInt(currentSeed));

    const activateTx = await consensusMain.connect(activator).activateTransaction(txId, vrfProofActivate);
    const activationReceipt = await activateTx.wait();
    const leaderAddress = consensusMain.interface.parseLog(activationReceipt.logs[0]).args[1];
    const leader = validators.find(v => v.address === leaderAddress);

    // 3. Propose receipt
    console.log("\n3. Proposing receipt...");
    const vrfProofPropose = await generateSignature(leader, BigInt(await consensusMain.recipientRandomSeed(ghostAddress)));
    await consensusMain.connect(leader).proposeReceipt(txId, "0x1234", [], vrfProofPropose);

    // 4. Commit votes
    console.log("\n4. Committing votes...");
    const voteType = 1; // Agree
    const nonces = [123, 456, 789];

    for (let i = 0; i < validators.length; i++) {
        const voteHash = ethers.solidityPackedKeccak256(
            ["address", "uint8", "uint256"],
            [validators[i].address, voteType, nonces[i]]
        );
        await consensusMain.connect(validators[i]).commitVote(txId, voteHash, false);
        console.log(`- Validator ${i + 1} committed vote`);
    }

    // 5. Reveal votes
    console.log("\n5. Revealing votes...");
    for (let i = 0; i < validators.length; i++) {
        const voteHash = ethers.solidityPackedKeccak256(
            ["address", "uint8", "uint256"],
            [validators[i].address, voteType, nonces[i]]
        );
        await consensusMain.connect(validators[i]).revealVote(txId, voteHash, voteType, nonces[i]);
        console.log(`- Validator ${i + 1} revealed vote`);
    }

    // 6. Finalize transaction
    console.log("\n6. Finalizing transaction...");
    await consensusMain.finalizeTransaction(txId);

    const finalStatus = await consensusMain.txStatus(txId);
    console.log("- Final transaction status:", finalStatus.toString());

    if (finalStatus.toString() === "6") {
        console.log("\n¡Consensus flow completed successfully! ✓");
    } else {
        throw new Error(`Unexpected final status: ${finalStatus}`);
    }
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });