from collections.abc import Generator

import ollama
from ollama import ChatResponse

MODEL = "exaone3.5:7.8b"


class FakerOrchestrator:
    def __init__(self, model: str = MODEL) -> None:
        self.model = model
        self.client = ollama.Client()

    def invoke(self, prompt: str) -> str:
        response: ChatResponse = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.message.content or ""

    def stream(self, prompt: str) -> Generator[str, None, None]:
        for chunk in self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        ):
            typed: ChatResponse = chunk
            yield typed.message.content or ""
