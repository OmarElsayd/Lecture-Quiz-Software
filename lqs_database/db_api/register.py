import logging
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_models.models import Users, Role, Class
from db_api.local_session import get_db
from db_api.api_util import get_hashed_password


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

router = APIRouter(
    prefix="/register",
    tags=["register"],
    responses={404: {"description": "Not found"}},
)


class  RegisterTemp(BaseModel):
    name: str
    email: str
    password: str
    course_code: str
    

class RegisterResponse(BaseModel):
    status: str
    message: Union[str, None]
    
    class Config:
        orm_mode = True
        
        
@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=RegisterResponse
)
def register(register_body: RegisterTemp, db:Session = Depends(get_db)):
    """ Register a new student

    Args:
        register_body (RegisterTemp): class containing name, email, password and course_code
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    
    try:
        password = get_hashed_password(register_body.password)
        responce = (db.query(Users).filter(Users.email == register_body.email).first())
        if responce:
            message="User already exists"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        if not responce:
            new_user = Users(
                name=register_body.name,
                email=register_body.email,
                password=password,
                role=Role.STUDENT
                )
            students_list = db.query(Class).filter(Class.course_code == register_body.course_code).first().student_list
            students_list.update({register_body.name : register_body.email})
            db.query(Class).filter(Class.course_code == register_body.course_code).update({"student_list":students_list})
            
            db.add(new_user)
            db.commit()

            message="User created successfully"
            return RegisterResponse(status=status.HTTP_200_OK, message=message)
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    
    
    