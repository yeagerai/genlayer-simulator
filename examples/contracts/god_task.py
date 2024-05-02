import json


class GodTask:

    def __init__(self, initial_completed_state):
        self.task_status = initial_completed_state
        self.gods_xpaths = {
            "Zeus": [
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[3]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[4]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[18]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[19]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[21]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[22]",
            ],
            "Hera": [
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[3]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[27]",
                "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[36]",
                "",
            ],
            "Poseidon": [],
            "Demeter": [],
            "Athena": [],
            "Apollo": [],
            "Artemis": [],
            "Ares": [],
            "Aphrodite": [],
            "Hephaestus": [],
            "Hermes": [],
            "Hestia": [],
            "Dionysus": [],
        }
        self.wikipedia_url = "https://en.wikipedia.org/wiki/"

    async def task(self, user_address: str, god: str, task: str) -> None:

        result_reasoning = "You can not do this task. You are not a Greek god"
        result_can_complete_task = False

        if god.title() in self.gods:
            url = self.wikipedia_url + god
            summary_prompt = "summarise the following page in 500 words or less"
            equivalence_criteria = "70 percent similarity"
            result = await self.query_webpage(url, summary_prompt, equivalence_criteria)
            result_json = json.loads(result)
            result_data = result_json["data"]

            prompt = f"""
You are the powerful Greek god {god}
{result_data}
and you need to {task}.
Can you do this?

Your response should be in the following format and valid JSON:
{{
    "reasoning": str,
    "task_completed": bool
}}
"reasoning" is to be a string of UNDER 200 words.
"""
            consensus_eq = "The result['task_completed'] must be exactly the same"
            result = await self.call_llm(prompt, consensus_eq=consensus_eq)
            result_json = json.loads(result)

            if result_json["task_completed"] is False:
                self.task_status = result["task_completed"]

            return {
                "reasoning": result_json["reasoning"],
                "can_complete_task": result_json["task_completed"],
                "state_updated": {"task_completed": self.task_status},
                "gas_used": self.gas_used,
            }

        return {
            "reasoning": result_reasoning,
            "can_complete_task": result_can_complete_task,
            "state_updated": {"task_completed": self.task_status},
            "gas_used": self.gas_used,
        }
