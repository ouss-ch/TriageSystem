"""Higher-level orchestration: ticket -> llm_service -> persisted TicketAnalysis."""

# TODO: load ticket, call llm_service.analyze_ticket_text, validate/normalize, save


def process_ticket(ticket_id: int) -> None:
    raise NotImplementedError
