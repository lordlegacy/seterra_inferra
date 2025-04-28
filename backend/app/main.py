from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import auth, tickets,users,llm,ingest_web_test
from app.llm.ingest import ingest_doc
from app.db import Base, engine
from dotenv import load_dotenv
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["Tickets"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["LLM"])
app.include_router(ingest_doc.router, prefix="/api/v1/llm", tags=["Ingestion"])
app.include_router(ingest_web_test.router, prefix="/api/v1/llm", tags=["Ingestion"])
