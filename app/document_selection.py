# document_selection.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import documents
from app.database import database

router = APIRouter()

class DocumentSelection(BaseModel):
    document_ids: list[int]

@router.post("/select_documents")
async def select_documents(doc_selection: DocumentSelection):
    selected_docs = []
    for doc_id in doc_selection.document_ids:
        query = documents.select().where(documents.c.id == doc_id)
        doc = await database.fetch_one(query)
        if doc:
            selected_docs.append(doc)
        else:
            raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    return {"selected_documents": selected_docs}
