import os

import requests
from openai import OpenAI


class LLMService:

    def __init__(self):

        self.provider = os.getenv("LLM_PROVIDER", "ollama")

        if self.provider == "openai":

            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )

            self.model = os.getenv(
                "OPENAI_MODEL",
                "gpt-4.1-mini"
            )

        else:

            self.base_url = os.getenv(
                "OLLAMA_URL",
                "http://ollama:11434"
            )

            self.model = os.getenv(
                "OLLAMA_MODEL",
                "llama3.2"
            )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.0
    ) -> str:

        if self.provider == "openai":

            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                temperature=temperature,
                max_output_tokens=300,
            )

            return response.output_text

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False,
                "options": {
                    "num_predict": 300
                }
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]