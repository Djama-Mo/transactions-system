from database import database_engine
from database.models import User

database_engine.Base.metadata.create_all(database_engine.engine)
