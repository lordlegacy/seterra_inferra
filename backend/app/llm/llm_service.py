from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.llm.query_engine import retrieve_context
from app.llm.client import call_llm  # we’ll stub this for now
from app.core.logger import logger

def build_prompt(ticket_text: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks[:10])  # limit for token safety
    return f"""
You are an AI helpdesk assistant.

The user submitted the following ticket:

\"\"\"{ticket_text}\"\"\"

Based on the following knowledge, summarize the issue, list the most likely causes, and recommend solutions.

Context:
{context}

Respond in JSON format like:
{{
  "summary": "...",
  "diagnosis": ["..."],
  "solutions": ["..."],
  "confidence": 0.87
}}
"""

def resolve_ticket(ticket_id: int, db: Session) -> dict:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return {"error": "Ticket not found"}

    full_text = f"{ticket.title}\n{ticket.description}"
    logger.info(f"Resolving ticket_id={ticket_id}")

    context_chunks = retrieve_context(db, full_text)

    prompt = build_prompt(full_text, context_chunks)
    logger.debug(f"Built prompt: {prompt[:500]}")  # log truncated for safety


    try:
        response_json = call_llm(prompt)  # will mock this for now
        logger.info("Calling LLM for ticket resolution")

        return response_json
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        return {
            "summary": "AI unavailable",
            "diagnosis": [],
            "solutions": [],
            "confidence": 0.0
        }
