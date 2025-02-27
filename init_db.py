# init_db.py
from app.database import engine
from app.models import metadata

metadata.create_all(engine)
