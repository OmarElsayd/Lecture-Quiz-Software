from sqlalchemy.orm import sessionmaker
from db_models.db_engine import create_db_engine

engine = create_db_engine()
LocalSession = sessionmaker(bind=engine)


