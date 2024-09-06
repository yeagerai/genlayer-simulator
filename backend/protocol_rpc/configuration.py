import os
import json

import requests


class GlobalConfiguration:
    @staticmethod
    def get_ollama_url(endpoint: str) -> str:
        return f"{os.environ['OLAMAPROTOCOL']}://{os.environ['OLAMAHOST']}:{os.environ['OLAMAPORT']}/api/{endpoint}"

    def get_disabled_info_logs_endpoints(self) -> list:
        return json.loads(os.environ.get("DISABLE_INFO_LOGS_ENDPOINTS", "[]"))

    def get_available_ollama_models(self) -> list:
        ollama_models_result = requests.get(self.get_ollama_url("tags")).json()
        installed_ollama_models = []
        for ollama_model in ollama_models_result["models"]:
            installed_ollama_models.append(ollama_model["name"].split(":")[0])
        return installed_ollama_models
