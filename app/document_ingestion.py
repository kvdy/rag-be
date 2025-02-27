# document_ingestion.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import documents
from app.database import database
from openai import OpenAI

client = OpenAI(api_key="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")
import numpy as np

router = APIRouter()


class DocumentIngestion(BaseModel):
    title: str
    content: str

@router.post("/ingest_document")
async def ingest_document(doc: DocumentIngestion):
    response = client.embeddings.create(model="text-embedding-ada-002",  # Use the appropriate model for embeddings
    input=doc.content)
    embedding = response.data[0].embedding
    embedding_bytes = np.array(embedding).tobytes()  # Convert embedding to bytes

    query = documents.insert().values(
        title=doc.title,
        content=doc.content,
        embedding=embedding_bytes
    )
    await database.execute(query)
    return {"message": "Document ingested successfully!"}
