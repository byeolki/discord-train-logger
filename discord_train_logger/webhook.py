import json
from pathlib import Path
from typing import Optional

import requests


class DiscordWebhook:
    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    def send(self, payload: dict) -> bool:
        try:
            resp = requests.post(self.url, json=payload, timeout=self.timeout)
            return resp.status_code in (200, 204)
        except Exception:
            return False

    def send_with_file(self, payload: dict, file_path: str, filename: Optional[str] = None) -> bool:
        path = Path(file_path)
        if not path.exists():
            return False

        name = filename or path.name
        try:
            with open(path, "rb") as f:
                resp = requests.post(
                    self.url,
                    data={"payload_json": json.dumps(payload)},
                    files={"file": (name, f)},
                    timeout=self.timeout,
                )
            return resp.status_code in (200, 204)
        except Exception:
            return False
