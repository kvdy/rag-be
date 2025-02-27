from sqlalchemy import Table, Column, Integer, String, LargeBinary, MetaData
from .database import metadata

metadata = MetaData()

documents = Table(
    "ingesteddocuments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("content", String, nullable=False),
    Column("embedding", LargeBinary, nullable=False),
)
