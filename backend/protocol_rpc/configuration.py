import os


class GlobalConfiguration:
    @staticmethod
    def get_ollama_url(endpoint: str) -> str:
        return f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"
