from sqlalchemy.orm import Session
from sqlalchemy import text, bindparam
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector  
from backend.app.llm.embedding import embed_single
from backend.app.models.ticket_embedding import TicketEmbedding
from backend.app.models.doc_chunk import DocChunk
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy import cast
from backend.app.core.logger import logger


# Optional fallback vector if embedding fails
def fake_vector(dim: int = 1536) -> list[float]:
    return [0.1] * dim



def search_ticket_embeddings(db: Session, query_vector: list[float], k: int = 5):
    from backend.app.core.logger import logger
    logger.info("Running ticket embedding search with k=%d", k)
    logger.debug(f"🔍 query_vector type: {type(query_vector)}")
    logger.debug(f"🔍 First 5 elements: {query_vector[:5]}")

    # Convert Python list to a string format PostgreSQL understands
    vector_str = "[" + ",".join(str(x) for x in query_vector) + "]"

    sql = text(f"""
        SELECT t.description
        FROM ticket_embeddings te
        JOIN tickets t ON t.id = te.ticket_id
        ORDER BY te.embedding <=> '{vector_str}'::vector
        LIMIT :k
    """)

    try:
        result = db.execute(sql, {"k": k})
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        logger.error(f"Ticket embedding search failed: {e}")
        return []



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
        query_vector = [float(x) for x in query_vector]
    except Exception:
        query_vector = fake_vector()
        logger.debug(f"Sanitized query_vector preview: {query_vector[:5]}")

    tickets = search_ticket_embeddings(db, query_vector, k)
    #docs = search_doc_chunks(db, query_vector, k)
    #web = search_web_snippets(db, query_vector, k)

    #return tickets + docs + web
    return tickets

