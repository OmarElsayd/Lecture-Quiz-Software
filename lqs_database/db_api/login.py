import logging
from enum import Enum
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_models.models import Users, Role
from db_api.local_session import get_db
from db_api.api_util import get_hashed_password


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)



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
        



@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
def login(login_body: LoginTemp, db: Session = Depends(get_db)):
    """
    Get email and password from the user and check if the user is an instructor or a student
    :param login_body:  email and password
    :param db:  database session
    :return:    status, role, message
    """
    try:
        password = get_hashed_password(login_body.password)
        
        response = (db.query(Users)
                    .filter(Users.email == login_body.email)
                    .filter(Users.password == password)
                    .first())
        if not response:
            login_response = LoginResponse(message="Incorrect email or password")
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role")
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)

