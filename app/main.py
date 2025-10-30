from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db import get_db, engine
from .models import Base, Document
from .tasks import embed_document


# Ensure metadata exists; in production use migrations (this is just convenience)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Vector Project API")


class DocumentCreate(BaseModel):
    content: str


class DocumentOut(BaseModel):
    id: str
    content: str


@app.post("/documents", response_model=DocumentOut)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    doc = Document(content=payload.content)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # enqueue embedding generation task asynchronously
    try:
        embed_document.delay(doc.id)
    except Exception:
        # if Celery isn't available, we still created the doc; embedding can be generated later
        pass

    return DocumentOut(id=doc.id, content=doc.content)


@app.get("/documents/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": doc.id,
        "content": doc.content,
        "embedding": doc.embedding,
        "created_at": doc.created_at,
    }
