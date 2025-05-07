from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.llm.embedding import embed_single
from backend.app.core.logger import logger

# Optional fallback vector if embedding fails
def fake_vector(dim: int = 1536) -> list[float]:
    return [0.1] * dim

def vector_to_pgstring(vec: list[float]) -> str:
    return "[" + ",".join(str(x) for x in vec) + "]"

def search_ticket_embeddings(db: Session, query_vector: list[float], k: int = 5):
    logger.info("Running ticket embedding search with k=%d", k)
    logger.debug(f"🔍 query_vector type: {type(query_vector)}")
    logger.debug(f"🔍 First 5 elements: {query_vector[:5]}")
    
    vector_str = vector_to_pgstring(query_vector)
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
    logger.info("Running doc chunk search with k=%d", k)
    logger.debug(f"🔍 First 5 elements: {query_vector[:5]}")
    
    vector_str = vector_to_pgstring(query_vector)
    sql = text(f"""
        SELECT chunk
        FROM doc_chunks
        ORDER BY embedding <=> '{vector_str}'::vector
        LIMIT :k
    """)
    try:
        result = db.execute(sql, {"k": k})
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        logger.error(f"Doc chunk search failed: {e}")
        return []

def search_web_snippets(db: Session, query_vector: list[float], k: int = 5):
    logger.info("Running web snippet search with k=%d", k)
    logger.debug(f"🔍 First 5 elements: {query_vector[:5]}")
    
    vector_str = vector_to_pgstring(query_vector)
    sql = text(f"""
        SELECT content
        FROM web_snippets
        ORDER BY embedding <=> '{vector_str}'::vector
        LIMIT :k
    """)
    try:
        result = db.execute(sql, {"k": k})
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        logger.error(f"Web snippet search failed: {e}")
        return []

def retrieve_context(db: Session, query: str, k: int = 5) -> list[str]:
    try:
        logger.info("Embedding query for retrieval")
        query_vector = embed_single(query)
        query_vector = [float(x) for x in query_vector]
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        query_vector = fake_vector()
        logger.debug(f"Sanitized query_vector preview: {query_vector[:5]}")

    tickets = search_ticket_embeddings(db, query_vector, k)
    docs = search_doc_chunks(db, query_vector, k)
    web = search_web_snippets(db, query_vector, k)

    return tickets + docs + web
