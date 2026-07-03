"""LLM client wrapper — sends ticket text, gets back structured analysis.

Talks to the local vLLM container (OpenAI-compatible /v1 API), not a hosted provider.
"""

# TODO: build openai.OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
#       client, model=settings.LLM_MODEL, prompt template, structured output parsing
#       (sentiment/category/keywords/priority)


def analyze_ticket_text(text: str) -> dict:
    raise NotImplementedError
