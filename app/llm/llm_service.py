import requests


class LLMService:

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2"
    ):
        self.base_url = base_url
        self.model = model

    def generate(
        self,
        prompt: str,
        temperature: float = 0.0
    ) -> str:
        """
        Sends the prompt to the LLM and returns the generated answer.
        """

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]