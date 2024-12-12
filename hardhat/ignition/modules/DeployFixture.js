const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

module.exports = buildModule("DeployFixture", (m) => {
    // 1. Deploy base contracts (in order of TransactionFlow)
    const ConsensusManager = m.contract("ConsensusManager");
    const GhostFactory = m.contract("GhostFactory");
    const GhostBlueprint = m.contract("GhostBlueprint");
    const GhostContract = m.contract("GhostContract");
    const MockGenStaking = m.contract("MockGenStaking", [m.getAccount(1)]);
    const Queues = m.contract("Queues");
    const Transactions = m.contract("Transactions");
    const ConsensusMain = m.contract("ConsensusMain");

    // 2. Initialize GhostFactory and configure GhostBlueprint
    const initGhostFactory = m.call(GhostFactory, "initialize");
    const setBlueprint = m.call(GhostFactory, "setGhostBlueprint", [GhostBlueprint], {
        after: [initGhostFactory]
    });

    // 3. Initialize ConsensusMain and dependents
    const initConsensusMain = m.call(ConsensusMain, "initialize", [ConsensusManager]);
    const initTransactions = m.call(Transactions, "initialize", [ConsensusMain], {
        after: [initConsensusMain]
    });
    const initQueues = m.call(Queues, "initialize", [ConsensusMain], {
        after: [initConsensusMain]
    });

    // 4. Setup contract connections
    m.call(ConsensusMain, "setGhostFactory", [GhostFactory], { after: [initConsensusMain] });
    m.call(ConsensusMain, "setGenStaking", [MockGenStaking], { after: [initConsensusMain] });
    m.call(ConsensusMain, "setGenQueue", [Queues], { after: [initConsensusMain, initQueues] });
    m.call(ConsensusMain, "setGenTransactions", [Transactions], { after: [initConsensusMain, initTransactions] });

    m.call(GhostFactory, "setGenConsensus", [ConsensusMain], { after: [initGhostFactory, initConsensusMain] });
    m.call(GhostFactory, "setGhostManager", [ConsensusMain], { after: [initGhostFactory, initConsensusMain] });
    m.call(Transactions, "setGenConsensus", [ConsensusMain], { after: [initTransactions] });
    m.call(ConsensusMain, "setAcceptanceTimeout", [0], { after: [initConsensusMain] });

    // 5. Setup validators
    const validator1 = m.getAccount(1);
    const validator2 = m.getAccount(2);
    const validator3 = m.getAccount(3);
    m.call(MockGenStaking, "addValidators", [[validator1, validator2, validator3]]);

    // 6. Deploy beacon proxy
    m.call(GhostFactory, "deployNewBeaconProxy", [], {
        after: [
            setBlueprint,
            initGhostFactory,
            initConsensusMain
        ]
    });

    return {
        GhostBlueprint,
        GhostContract,
        ConsensusManager,
        GhostFactory,
        MockGenStaking,
        Queues,
        Transactions,
        ConsensusMain
    };
});