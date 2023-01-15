from sqlalchemy.orm import sessionmaker
from lqs_database.db_models.db_engine import create_db_engine


def set_session() -> sessionmaker:
    """
    Create a session to the database
    :return:    sessionmaker
    """
    engine = create_db_engine()
    session = sessionmaker(bind=engine)
    return session

