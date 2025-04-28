from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.ticket_embedding import TicketEmbedding
from app.models.doc_chunk import DocChunk
from app.models.web_snippet import WebSnippet
from app.llm.embedding import embed_single  # assumed working

# Optional: fallback if embedding fails (mock)
def fake_vector(dim: int = 1536) -> list[float]:
    return [0.1] * dim

def search_ticket_embeddings(db: Session, query_vector: list[float], k: int = 5) -> list[str]:
    sql = text(f"""
        SELECT t.description FROM ticket_embeddings te
        JOIN tickets t ON t.id = te.ticket_id
        ORDER BY te.embedding <=> :vector
        LIMIT :k
    """)
    result = db.execute(sql, {"vector": query_vector, "k": k})
    return [row[0] for row in result.fetchall()]

def search_doc_chunks(db: Session, query_vector: list[float], k: int = 5) -> list[str]:
    sql = text(f"""
        SELECT chunk FROM doc_chunks
        ORDER BY embedding <=> :vector
        LIMIT :k
    """)
    result = db.execute(sql, {"vector": query_vector, "k": k})
    return [row[0] for row in result.fetchall()]

def search_web_snippets(db: Session, query_vector: list[float], k: int = 5) -> list[str]:
    sql = text(f"""
        SELECT content FROM web_snippets
        ORDER BY embedding <=> :vector
        LIMIT :k
    """)
    result = db.execute(sql, {"vector": query_vector, "k": k})
    return [row[0] for row in result.fetchall()]

def retrieve_context(db: Session, query: str, k: int = 5) -> list[str]:
    try:
        query_vector = embed_single(query)  # real embedding
    except Exception:
        query_vector = fake_vector()

    tickets = search_ticket_embeddings(db, query_vector, k)
    docs = search_doc_chunks(db, query_vector, k)
    web = search_web_snippets(db, query_vector, k)

    return tickets + docs + web
