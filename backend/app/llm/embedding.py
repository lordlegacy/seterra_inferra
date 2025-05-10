from dotenv import load_dotenv
from langchain_nomic import NomicEmbeddings
import os



load_dotenv() 

nomic = NomicEmbeddings(model="nomic-embed-text-v1.5")

def embed_texts(texts: list[str]) -> list[list[float]]:
    return nomic.embed_documents(texts)

def embed_query(query: str) -> list[float]:
    return nomic.embed_query(query)
