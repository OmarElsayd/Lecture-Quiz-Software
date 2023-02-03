import logging
from enum import Enum
from typing import Generator, Union
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_models import set_session
from db_models.models import Users, Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)


def get_db() -> Generator:
    db = set_session.LocalSession()
    try:
        yield db
        db.commit()
    finally:
        db.close()


class LoginTemp(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    status: bool = False
    is_instructor: bool = False
    role: Union[Enum, None] = None
    message: Union[str, None]

    class Config:
        orm_mode = True


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
def get_email(login_body: LoginTemp = Depends(), db: Session = Depends(get_db)):
    """
    Get email and password from the user and check if the user is an instructor or a student
    :param login_body:  email and password
    :param db:  database session
    :return:    status, role, message
    """
    try:
        response = (db.query(Users)
                    .filter(Users.email == login_body.email)
                    .filter(Users.password == login_body.password)
                    .first())
        if not response:
            login_response = LoginResponse(message="Not a user. Please register")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(login_response.message))
        if response.role.value in (
                Role.INSTRUCTOR.value,
                Role.TA.value
        ):
            return LoginResponse(
                status=True,
                role=response.role,
                is_instructor=True,
                message=f"Login Successful for instructor! Welcome {response.name}"
            )
        if response.role.value == Role.STUDENT.value:
            return LoginResponse(
                status=True,
                role=response.role,
                is_instructor=False,
                message=f"Login Successful! Welcome {response.name}"
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role:")
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)

