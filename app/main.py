from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import database
from app.document_ingestion import router as document_ingestion_router
from app.qa_api import router as qa_api_router
from app.document_selection import router as document_selection_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(document_ingestion_router, prefix="/api")
app.include_router(qa_api_router, prefix="/api")
app.include_router(document_selection_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
