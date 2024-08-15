import os
import json


class GlobalConfiguration:
    @staticmethod
    def get_ollama_url(endpoint: str) -> str:
        return f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"

    def get_disabled_info_logs_endpoints(self) -> list:
        return json.loads(os.environ.get("DISABLE_INFO_LOGS_ENDPOINTS", "[]"))
