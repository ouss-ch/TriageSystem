"""LLM client wrapper — sends ticket text, gets back structured analysis."""

# TODO: build client from settings.LLM_PROVIDER / LLM_API_KEY / LLM_MODEL,
#       prompt template, structured output parsing (sentiment/category/keywords/priority)


def analyze_ticket_text(text: str) -> dict:
    raise NotImplementedError
