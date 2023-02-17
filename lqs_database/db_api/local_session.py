
from typing import Generator
from db_models import set_session

def get_db() -> Generator:
    """Get a database session

    Yields:
        Generator:  A database session
    """
    db = set_session.LocalSession()
    try:
        yield db
        db.commit()
    finally:
        db.close()
        
        
