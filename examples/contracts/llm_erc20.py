import json
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple


class LlmErc20(IContract):
    def __init__(self, total_supply: int) -> None:
        self.balances = {}
        self.balances[contract_runner.from_address] = total_supply

    async def transfer(self, amount: int, to_address: str) -> None:
        prompt = f"""
You keep track of transactions between users and their balance in coins.
The current balance for all users in JSON format is:
{json.dumps(self.balances)}
The transaction to compute is: {{
sender: "{contract_runner.from_address}",
recipient: "{to_address}",
amount: {amount},
}}

For every transaction, validate that the user sending the Coins has
enough balance. If any transaction is invalid, it shouldn't be processed.
Update the balances based on the valid transactions only.
Given the current balance in JSON format and the transaction provided,
please provide the result of your calculation with the following format:
{{
"transaction_success": bool,          // Whether the transaction was successful
"transaction_error": str,             // Empty if transaction is successful
"updated_balances": object<str, int>  // Updated balances after the transaction
}}
It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
This result should be perfectly parseable by a JSON parser without errors."""
        print(prompt)
        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="""The new_balance of the sender should have decreased
            in the amount sent and the new_balance of the receiver should have
            increased by the amount sent. Also, the total sum of all balances
            should have remain the same before and after the transaction""",
            comparative=True,
        ) as eq:
            result = await eq.call_llm(prompt)
            result_clean = result.replace("True", "true").replace("False", "false")
            eq.set(result_clean)

        print("final_result: ", final_result)
        print("final_result[output]: ", final_result["output"])
        result_json = json.loads(final_result["output"])
        self.balances = result_json["updated_balances"]

    def get_balances(self) -> dict[str, int]:
        return self.balances

    def get_balance_of(self, address: str) -> int:
        return self.balances.get(address, 0)
