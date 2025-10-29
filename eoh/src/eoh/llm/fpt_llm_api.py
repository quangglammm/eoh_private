import json
from urllib.parse import urljoin
import requests


class FPTInterfaceAPI:
    def __init__(self, api_endpoint, api_key, model_LLM, debug_mode):
        self.api_endpoint = (api_endpoint or "").rstrip("/")
        if self.api_endpoint and not self.api_endpoint.startswith("http"):
            self.api_endpoint = "https://" + self.api_endpoint
        self.api_key = api_key
        self.model_LLM = model_LLM
        self.debug_mode = debug_mode
        self.n_trial = 5

    def get_response(self, prompt_content):
        url = urljoin(self.api_endpoint + "/", "v1/chat/completions")
        payload = {
            "model": self.model_LLM,
            "messages": [
                {"role": "user", "content": prompt_content}
            ],
            # Defaults aligned with provided template
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response_text = None
        attempt = 0
        while attempt < self.n_trial:
            attempt += 1
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
                if resp.status_code != 200:
                    if self.debug_mode:
                        print(f"[LLM API] HTTP {resp.status_code}")
                    continue
                data = resp.json()
                response_text = data["choices"][0]["message"]["content"]
                break
            except Exception as e:
                if self.debug_mode:
                    print(f"[LLM API] Exception: {e}")
                continue

        print(f"[DEBUG] response: {response_text}")
        return response_text


