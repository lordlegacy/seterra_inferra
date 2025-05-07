from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.deps import get_db
from backend.app.llm.chunking import chunk_text
from backend.app.llm.embedding import embed_texts
from backend.app.models.doc_chunk import DocChunk

import pdfplumber
import docx
import io

router = APIRouter()

def extract_text_from_pdf(file: UploadFile) -> str:
    with pdfplumber.open(file.file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file: UploadFile) -> str:
    doc = docx.Document(file.file)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_md(file: UploadFile) -> str:
    content = file.file.read().decode('utf-8')
    return content

def parse_file(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.filename.endswith(".docx"):
        return extract_text_from_docx(file)
    elif file.filename.endswith(".md"):
        return extract_text_from_md(file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

@router.post("/ingest_doc/")
async def ingest_doc(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        raw_text = parse_file(file)
        chunks = chunk_text(raw_text)
        embeddings = embed_texts(chunks)

        for chunk, embedding in zip(chunks, embeddings):
            doc_entry = DocChunk(
                source=file.filename,
                chunk=chunk,
                embedding=embedding
            )
            db.add(doc_entry)

        db.commit()
        return {"msg": f"{len(chunks)} chunks embedded and stored from {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")
