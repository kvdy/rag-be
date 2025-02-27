# qa_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import documents
from app.database import database
from openai import OpenAI

client = OpenAI(api_key="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")



import numpy as np
from scipy.spatial.distance import cosine

router = APIRouter()


class QARequest(BaseModel):
    question: str

def cosine_similarity(a, b):
    return 1 - cosine(a, b)

@router.post("/ask_question")
async def ask_question(qa_request: QARequest):
    query = documents.select()
    docs = await database.fetch_all(query)
    embeddings = [np.frombuffer(doc["embedding"], dtype=np.float32) for doc in docs]

    # Generate embedding for the question
    response = client.embeddings.create(model="text-embedding-ada-002",
    input=qa_request.question)
    question_embedding = np.array(response.data[0].embedding, dtype=np.float32)

    # Ensure all embeddings have the same dimension
    if question_embedding.shape[0] != embeddings[0].shape[0]:
        raise HTTPException(status_code=500, detail="Embedding dimension mismatch")

    # Find the most relevant document
    similarities = [cosine_similarity(question_embedding, emb) for emb in embeddings]
    most_relevant_index = np.argmax(similarities)
    most_relevant_doc = docs[most_relevant_index]

    # Use the content of the most relevant document to generate an answer
    answer_response = client.completions.create(model="text-davinci-003",
    prompt=f"Answer the question based on the following document content:\n\n{most_relevant_doc['content']}\n\nQuestion: {qa_request.question}\nAnswer:",
    max_tokens=150)
    answer = answer_response.choices[0].text.strip()
    return {"answer": answer}
