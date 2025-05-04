from sqlalchemy.orm import Session
from sqlalchemy import text, bindparam
from sqlalchemy.dialects.postgresql import ARRAY
from app.llm.embedding import embed_single
from app.models.ticket_embedding import TicketEmbedding
from app.models.doc_chunk import DocChunk
from app.core.logger import logger


# Optional fallback vector if embedding fails
def fake_vector(dim: int = 1536) -> list[float]:
    return [0.1] * dim

# ✅ FIXED: Typed binding for pgvector and integer param
def search_ticket_embeddings(db: Session, query_vector: list[float], k: int = 5):
    sql = text("""
        SELECT t.description
        FROM ticket_embeddings te
        JOIN tickets t ON t.id = te.ticket_id
        ORDER BY te.embedding <=> CAST(:vector AS vector)
        LIMIT :k
    """).bindparams(
        bindparam("vector", type_=ARRAY(float)),
        bindparam("k", type_=int)
    )
    result = db.execute(sql, {"vector": query_vector, "k": k})
    return [row[0] for row in result.fetchall()]

def search_doc_chunks(db: Session, query_vector: list[float], k: int = 5):
    sql = text("""
        SELECT chunk
        FROM doc_chunks
        ORDER BY embedding <=> CAST(:vector AS vector)
        LIMIT :k
    """).bindparams(
        bindparam("vector", type_=ARRAY(float)),
        bindparam("k", type_=int)
    )
    result = db.execute(sql, {"vector": query_vector, "k": k})
    return [row[0] for row in result.fetchall()]

def search_web_snippets(db: Session, query_vector: list[float], k: int = 5):
    sql = text("""
        SELECT content
        FROM web_snippets
        ORDER BY embedding <=> CAST(:vector AS vector)
        LIMIT :k
    """).bindparams(
        bindparam("vector", type_=ARRAY(float)),
        bindparam("k", type_=int)
    )
    result = db.execute(sql, {"vector": query_vector, "k": k})
    return [row[0] for row in result.fetchall()]

def retrieve_context(db: Session, query: str, k: int = 5) -> list[str]:
    try:
        query_vector = embed_single(query)
    except Exception:
        query_vector = fake_vector()

    tickets = search_ticket_embeddings(db, query_vector, k)
    docs = search_doc_chunks(db, query_vector, k)
    web = search_web_snippets(db, query_vector, k)

    return tickets + docs + web
