from asyncio import Queue
from backend.database_handler.domain.state import State
from backend.consensus.vrf import get_validators_for_transaction
from backend.node.base import Node
from backend.database_handler.types import ConsensusData
from time import sleep


class ConsensusAlgorithm:
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.queues = {}

    def crawl_snapshot(self):
        last_block_num = self.snapshot.last_block_num
        while True:
            blocks = self.snapshot.get_last_blocks(last_block_num, status="initial")
            if len(blocks > 0):
                for block in blocks:
                    transaction_input = block["transaction_input"]
                    contract_address = transaction_input["contract_address"]
                    last_block_num = block["block_num"]
                    try:
                        self.queues[contract_address].put(block)
                    except KeyError:
                        self.queues[contract_address] = Queue()
                        self.queues[contract_address].put(block)
            sleep(10)

    def run_consensus(self):
        while True:
            sleep(10)

    async def exec_transaction(
        self,
        from_address: str,
        transaction_input: dict,
        snapshot: State,
    ) -> dict:
        contract_address = transaction_input["contract_address"]

        # assign execution queue

        all_validators = snapshot.validators_db_service.get_all_validators()
        leader, remaining_validators = get_validators_for_transaction(
            all_validators, snapshot.num_validators
        )
        num_validators = len(remaining_validators) + 1

        leader_node = Node(snapshot, leader["address"], "leader", leader["config"])
        leader_receipt = leader_node.exec_transaction(
            from_address, contract_account_data["data"], transaction_input["args"]
        )
        votes = {leader["address"]: leader_receipt["vote"]}

        validator_nodes = [
            Node(validator["address"], "validator", validator["config"], leader_receipt)
            for i, validator in enumerate(remaining_validators)
        ]

        validators_results = []
        for validator in validator_nodes:
            validator_receipt = validator.exec_transaction(
                from_address,
                contract_account_data["data"],
                transaction_input["function_name"],
                transaction_input["args"],
            )
            votes[validator["address"]] = validator_receipt["vote"]
            validators_results.append(validator_receipt)

        # TODO: check if half of the validators agree with the leader or raise an exception
        if (
            len([vote for vote in votes.values() if vote == "agree"])
            < num_validators // 2
        ):
            raise Exception("Consensus not reached")

        # Validators execute transaction
        # loop = asyncio.get_running_loop()
        # validation_tasks = [
        #     loop.create_task(validator_executes_transaction(transaction_input, leader_receipt, validator)) # watch out! as ollama uses GPU resources
        #     for validator in remaining_validators
        # ]
        # validation_results = await asyncio.gather(*validation_tasks)

        # for i in range(len(validation_results)):
        #     votes[f"{validation_results[i]['validator']}"] = validation_results[i]["vote"]

        final = False
        consensus_data = ConsensusData(
            final=final,
            votes=votes,
            leader=leader_receipt,
            validators=validators_results,
        ).model_dump_json()

        execution_output = {}
        execution_output["leader_data"] = leader_receipt
        execution_output["consensus_data"] = consensus_data
        return execution_output
