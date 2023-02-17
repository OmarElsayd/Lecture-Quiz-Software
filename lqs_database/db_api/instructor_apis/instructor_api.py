import logging
from db_api.local_session import get_db
from fastapi import Depends, HTTPException, status
from typing import List
from sqlalchemy import delete
from sqlalchemy.orm import Session
from .classes_util import Students, genResponce, ClassInput
from db_models.models import Class, Users, Role
from fastapi import APIRouter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

router = APIRouter(
    prefix="/instructor",
    tags=["instructor"],
    responses={404: {"description": "Not found"}}
)



@router.get(
    "/getAllStudents",
    status_code=status.HTTP_200_OK,
    response_model=List[Students]
)
def get_all_students(session: Session = Depends(get_db)):
    """ 
    Get all students in the class from the database
    Args:
        session (Session, optional): Database session. Defaults to Depends(get_db).
    """
    try:
        students = session.query(Users).filter(
            Users.role == Role.STUDENT.value
            ).all()
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No students found")
        students_list = []
        for student in students:
            students_list.append(Students(
                name=student.name,
                email=student.email
            ))
        return students_list
    except HTTPException:
        raise
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    
    

@router.delete(
    "/deleteUser",
    status_code=status.HTTP_200_OK,
    response_model=genResponce
)
def delete_user(
    input_body: Students,
    session: Session = Depends(get_db)
):
    try:
        delete_stmt = (
            delete(Users).
            where(Users.email == input_body.email)
        )
        resultes = session.execute(delete_stmt)
        if resultes.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No student found")
        return genResponce(status=True, message="Student deleted successfully")
    except HTTPException:
        raise
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
      
      
@router.post(
    "/NewClass",
    status_code=status.HTTP_200_OK,
    response_model=genResponce
)
def create_new_clas(
    input_body: ClassInput,
    session: Session = Depends(get_db)
):
    try:
        if not input_body.class_name or not input_body.course_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Class name and course code are required"
                )
        new_class = Class(
            class_name=input_body.class_name,
            course_code=input_body.course_code,
            instructor_id=input_body.instructor_id,
            student_list=dict()
        )
        session.add(new_class)
        session.commit()
        return genResponce(status=True, message="Class created successfully")
    except HTTPException:
        raise
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error{error}")
            

