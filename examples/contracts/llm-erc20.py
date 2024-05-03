import json
from genvm.base.equivalence_principle import EquivalencePrinciple


class WizzardOfCoin:
    prompt_part_1: str = """You keep track of transactions between users 
    and their balance in coins. 
    The current balance for all users in JSON format is:"""

    prompt_part_2: str = "The transaction to compute is:"

    prompt_part_3: str = """Given the current balance in JSON format and 
    the transaction provided, please provide the updated balances as a 
    JSON object.
    For every transaction, validate that the user sending the Coins has 
    enough balance. If any transaction is invalid it shouldn't be processed. 
    Update the balances based on the valid transactions only.
    It is mandatory that you respond with only the JSON balances object, nothing 
    else whatsoever. Don't include any other words or characters, your 
    output must be only the balances JSON object"""

    def __init__(self, initial_owner: str, total_supply: int):
        super().__init__()
        self.balances = {}
        self.balances[initial_owner] = total_supply

    async def send(self, amount: int, from_address: str, to_address: str) -> None:
        prompt = f"""
{self.prompt_part_1}
{json.dumps(self.balances)}
{self.prompt_part_2}
{from_address} sends {amount} coins to {to_address}
{self.prompt_part_3}"""
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
            result_json = json.loads(result_clean)
            eq.set(result_json)

        self.balances = final_result["output"]

    
    def get_balances(self):
        return self.balances
