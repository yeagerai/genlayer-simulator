import os
import json


class GlobalConfiguration:
    @staticmethod
    def get_ollama_url(endpoint: str) -> str | None:
        protocol = os.environ.get("OLAMAPROTOCOL")
        host = os.environ.get("OLAMAHOST")
        port = os.environ.get("OLAMAPORT")
        if not protocol or not host or not port:
            return None
        return f"{protocol}://{host}:{port}/api/{endpoint}"

    def get_disabled_info_logs_endpoints(self) -> list:
        return json.loads(os.environ.get("DISABLE_INFO_LOGS_ENDPOINTS", "[]"))
