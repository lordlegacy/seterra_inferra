from dotenv import load_dotenv
load_dotenv() 
from langchain_nomic import NomicEmbeddings
import os



embedder = NomicEmbeddings(
    model="nomic-embed-text-v1.5",
    # You can optionally set dimensionality (default 768)
    # dimensionality=768,
    # inference_mode="remote" (default)
)

def embed_texts(texts: list[str]) -> list[list[float]]:
    return embedder.embed_documents(texts)

def embed_single(text: str) -> list[float]:
    return embedder.embed_query(text)
