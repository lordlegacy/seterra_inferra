from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.llm.ingest.ingest_web import ingest_web_for_ticket

router = APIRouter()
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

@router.post("/test_ingest_web/")
def test_ingest_web(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        ingest_web_for_ticket(db, request.query)
        return {"msg": f"Ingested web snippets for query '{request.query}' successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")
