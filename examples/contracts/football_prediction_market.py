import json
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple


class PredictionMarket(IContract):
    def __init__(self, game_date: str, team1: str, team2: str):
        """
        Initializes a new instance of the prediction market with the specified game date and teams.

        Args:
            game_date (str): The date of the game in the format 'YYYY-MM-DD'.
            team1 (str): The name of the first team.
            team2 (str): The name of the second team.

        Attributes:
            has_resolved (bool): Indicates whether the game's resolution has been processed. Default is False.
            game_date (str): The date of the game.
            resolution_url (str): The URL to the game's resolution on BBC Sport.
            team1 (str): The name of the first team.
            team2 (str): The name of the second team.
        """
        self.has_resolved = False
        self.game_date = game_date
        self.resolution_url = (
            "https://www.bbc.com/sport/football/scores-fixtures/" + game_date
        )
        self.team1 = team1
        self.team2 = team2

    async def resolve(self) -> None:

        if self.has_resolved:
            return "Already resolved"

        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="The score and the winner has to be exactly the same",
            comparative=True,
        ) as eq:
            web_data = await eq.get_webpage(self.resolution_url)
            print(web_data)

            task = f"""In the following web page, find the winning team in a matchup between the following teams:
            Team 1: {self.team1}
            Team 2: {self.team2}

            Web page content:
            {web_data}
            End of web page data.

            If it says "Kick off [time]" between the names of the two teams, it means the game hasn't started yet.
            If you fail to extract the score, assume the game is not resolved yet.

            Respond with the following JSON format:
            {{
                "score": str, // The score with numbers only, e.g, "1:2", or "-" if the game is not resolved yet
                "winner": int, // The number of the winning team, 0 for draw, or -1 if the game is not yet finished
            }}
            It is mandatory that you respond only using the JSON format above,
            nothing else. Don't include any other words or characters,
            your output must be only JSON without any formatting or quotes of any kind.
            """
            result = await eq.call_llm(task)
            print(result)
            eq.set(result)

        result_json = json.loads(final_result["output"])

        if result_json["winner"] > -1:
            self.has_resolved = True
            self.winner = result_json["winner"]
            self.score = result_json["score"]

        return result_json
