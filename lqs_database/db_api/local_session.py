
from contextlib import contextmanager
import logging
from typing import Generator
from db_models import set_session
from fastapi import HTTPException, status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

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
        
@contextmanager
def transaction(session):
    """Transaction context manager

    Args:
        session (Session): Database session

    Raises:
        HTTPException: Internal Server Error

    Yields:
        _type_:     Database session
    """
    try:
        yield session
        session.commit()
    except Exception as error:
        logger.error(error)
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error {error}")
    finally:
        session.close()
        
        
