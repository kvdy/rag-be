# document_ingestion.py

# OPENAI_API_KEY=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

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.models import documents
from app.database import database
from openai import OpenAI
import numpy as np

client = OpenAI(api_key="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")

router = APIRouter()

class DocumentIngestion(BaseModel):
    title: str
    content: str

def split_document_into_chunks(content: str, chunk_size: int = 512):
    words = content.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

async def generate_and_store_embedding(title: str, chunk: str, chunk_id: int):
    response = client.embeddings.create(model="text-embedding-ada-002", input=chunk)
    embedding = response.data[0].embedding
    embedding_bytes = np.array(embedding).tobytes()  # Convert embedding to bytes

    query = documents.insert().values(
        title=f"{title}_chunk_{chunk_id}",
        content=chunk,
        embedding=embedding_bytes
    )
    await database.execute(query)

@router.post("/ingest_document")
async def ingest_document(file: UploadFile = File(...)):
    content = await file.read()
    content_str = content.decode()
    chunks = split_document_into_chunks(content_str)

    for i, chunk in enumerate(chunks):
        await generate_and_store_embedding(file.filename, chunk, i)

    return {"message": "Document ingested and split into chunks successfully!"}
