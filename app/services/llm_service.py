"""LLM client wrapper — sends ticket text, gets back structured analysis.

Talks to the local vLLM container (OpenAI-compatible /v1 API), not a hosted provider.
Structured output relies on vLLM's guided-decoding support for response_format —
confirm the served model backs that before relying on it in production.
"""

from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from app.core.config import settings

T = TypeVar("T", bound=BaseModel)


class Assistant:
    """An LLM client bound to one system prompt and a fixed set of call configs."""

    def __init__(self, system_prompt: str, model: str = settings.LLM_MODEL, **configs):
        self._client = OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
        self._system_prompt = system_prompt
        self._model = model
        self._configs = configs

    def invoke(self, structured_output: type[T], query: str) -> T:
        """Run query through the assistant, parsed into structured_output."""
        completion = self._client.beta.chat.completions.parse(
            model=self._model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": query},
            ],
            response_format=structured_output,
            **self._configs,
        )
        return completion.choices[0].message.parsed


def create_assistant(system_prompt: str, **configs) -> Assistant:
    return Assistant(system_prompt, **configs)
