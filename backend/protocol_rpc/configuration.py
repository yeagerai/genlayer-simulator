import os
import json


class GlobalConfiguration:
    @staticmethod
    def get_disabled_info_logs_endpoints() -> list:
        return json.loads(os.environ.get("DISABLE_INFO_LOGS_ENDPOINTS", "[]"))
