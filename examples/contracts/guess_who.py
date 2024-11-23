# { "Depends": "py-genlayer:test" }

import json
from genlayer import *


@gl.contract
class GuessWho:
    category: str
    questions: list[tuple[str, str]]
    character: str

    def __init__(self, category: str):
        self.category = category
        self.questions = []
        self.character = ""

    @gl.public.write
    def ask_question(self) -> None:
        prompt = f"""
        You are playing "Guess Who?" game, trying to guess a character from the category: {self.category}.
        Given the past questions and answers:
        {self.questions}
        
        Create a new question such that:
        - is different from the past questions.
        - is a yes/no question.
        - helps narrow down the possible characters.
        """

        result = gl.eq_principle_prompt_comparative(
            prompt,
            "Create a new question that is a yes/no question",
        )

    @gl.public.write
    def answer_question(self, answer: bool) -> None:
        prompt = f"""
You are trying to guess a character from the category: {self.category}.
Here are the questions asked so far:
{json.dumps(self.questions)}
The user's answer to the last question is: {"yes" if answer else "no"}.

Based on the questions and answers, try to guess the character the user is thinking of.
Respond with the following JSON format:
{{
    "guess": str, // The name of the character you think the user is thinking of
    "confidence": float // A confidence score between 0 and 1
}}
It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
This result should be perfectly parsable by a JSON parser without errors.
"""

        def run():
            res = gl.exec_prompt(prompt)
            res = res.replace("```json", "").replace("```", "")
            return res

        final_result = gl.eq_principle_prompt_comparative(
            run, "Make a guess based on the questions and answers provided."
        )
        result_json = json.loads(final_result)
        self.character = result_json["guess"]

    @gl.public.view
    def get_character(self) -> str:
        return self.character

    @gl.public.view
    def get_questions(self) -> list[str]:
        return self.questions
