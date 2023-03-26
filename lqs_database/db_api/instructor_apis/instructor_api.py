from datetime import datetime
import json
import logging
import pandas as pd
from db_api.api_util import create_quiz_code, get_hashed_password, validate_email
from db_api.local_session import get_db, transaction
from fastapi import Depends, HTTPException, Response, WebSocket, WebSocketDisconnect, status
from typing import List
from sqlalchemy import delete
from sqlalchemy.orm import Session
from .classes_util import CreateQuestionInput, CreateQuizInput, CreateQuizResponse, QuizData, Students, TaTemplete, WebSocketManager, genResponse, ClassInput
from db_models.models import Class, Lectures, QuestionAnswers, QuestionType, Questions, Quizzes, Responses, Users, Role
from fastapi import APIRouter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

router = APIRouter(
    prefix="/instructor",
    tags=["instructor"],
    responses={404: {"description": "Not found"}}
)

manager = WebSocketManager()



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
    response_model=genResponse
)
def delete_user(
    input_body: Students,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(Users).filter_by(email=input_body.email, name=input_body.name).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No student found")
        db.delete(user)
        db.commit()
        return genResponse(status=True, message="Student deleted successfully")
    except HTTPException:
        raise
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

      
      
@router.post(
    "/NewClass",
    status_code=status.HTTP_200_OK,
    response_model=genResponse
)
def create_new_clas(
    input_body: ClassInput,
    session: Session = Depends(get_db)
):
    if session.query(Class).filter(Class.course_code == input_body.course_code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
            )
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
        return genResponse(status=True, message="Class created successfully")
    except HTTPException:
        raise
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error{error}")
            

@router.put(
    "/create_ta",
    status_code=status.HTTP_200_OK,
    response_model=genResponse
)
def create_ta_user(
    input_body: TaTemplete,
    session: Session = Depends(get_db)
):
    if not input_body.name or not input_body.email or not input_body.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name, email and password are required"
            )
    if not validate_email(input_body.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email! Use school email"
            )
    password = get_hashed_password(input_body.password)
    try:
        new_ta = Users(
            name=input_body.name,
            email=input_body.email,
            password=password,
            role=Role.TA.value
            )
        session.add(new_ta)
        session.commit()
        return genResponse(status=True, message="TA created successfully")
    
    except HTTPException:
        raise
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error {error}")
    
    
@router.put("/create_quiz", status_code=status.HTTP_200_OK, response_model=CreateQuizResponse)
def create_quiz(
    quiz_header: CreateQuizInput,
    questions: List[CreateQuestionInput],
    session: Session = Depends(get_db)
):
    try:
        class_query = session.query(Class).filter(Class.course_code == quiz_header.class_code).first()
        with transaction(session) as tx:
            new_lecture = Lectures(
                lecture_name=quiz_header.lecture_name,
                class_id=class_query.id,
                lecture_date=quiz_header.lecture_date,
                user_id=class_query.instructor_id,
            )
            tx.add(new_lecture)
            tx.flush()
            new_quiz_header = Quizzes(
                quiz_name=create_quiz_code(),
                number_of_questions=quiz_header.number_of_questions,
                quiz_duration=quiz_header.quiz_duration,
                lecture_id=new_lecture.id
            )
            tx.add(new_quiz_header)
            tx.flush()

            quiz_id = new_quiz_header.id
            quiz_code = new_quiz_header.quiz_name

            for index, question in enumerate(questions):
                add_question = Questions(
                    question_order=index,
                    question_type=QuestionType(question.question_type).name,
                    question=question.question,
                    quiz_id=quiz_id,
                    correct_answer=question.correct_answer
                )
                tx.add(add_question)
                tx.flush()
                question_id = add_question.id

                if question.question_type == QuestionType.MultipleChoice.value:
                    option1 = QuestionAnswers(
                        answer=question.option1,
                        question_id=question_id
                    )
                    option2 = QuestionAnswers(
                        answer=question.option2,
                        question_id=question_id
                    )
                    option3 = QuestionAnswers(
                        answer=question.option3,
                        question_id=question_id
                    )
                    option4 = QuestionAnswers(
                        answer=question.option4,
                        question_id=question_id
                    )
                    tx.add_all([option1, option2, option3, option4])
                    tx.flush()
                elif question.question_type == QuestionType.TrueFalse.value:
                    answer = QuestionAnswers(
                        answer=question.correct_answer,
                        question_id=question_id
                    )
                    tx.add(answer)
                    tx.flush()

            return CreateQuizResponse(
                status=True,
                message="Quiz created successfully",
                quiz_id=quiz_id,
                quiz_code=quiz_code
                )

    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error {error}")
    
    
@router.get(
    "/all_courses",
    status_code=status.HTTP_200_OK,
)
def get_all_courses(session: Session = Depends(get_db)):
    """
    
    """
    results = session.query(Class.course_code).all()
    course_codes = [row[0] for row in results] 
    return course_codes
    
    
@router.websocket("/start_quiz_ws")
async def start_quiz_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            logger.info("Waiting for event")
            event = await websocket.receive_text()
            logger.info(f"Received event: {event}")
            if event == '"start"':
                logger.info(f"Received event: {event}")
                await manager.broadcast(json.dumps({'event': 'start_quiz'}))
    except WebSocketDisconnect as e:
        logger.info(f"WebSocket disconnected with code: {e}")
    finally:
        await manager.disconnect(websocket)
        
        
@router.get(
    "/download_quiz/{quiz_id}",
    status_code=status.HTTP_200_OK,
    )
def donwload_quiz_resultes(quiz_id: str, session: Session = Depends(get_db)):
    """_summary_

    Args:
        quiz_id (int): _description_
        session (Session, optional): _description_. Defaults to Depends(get_db).
    """
    try:
        logger.info(quiz_id)
        quiz_results = session.query(
            Users.name.label("Student Name"),
            Quizzes.id.label("quiz id"),
            Quizzes.quiz_name.label("Quiz Name"),
            Quizzes.quiz_duration,
            Questions.id.label("question_id"),
            Questions.question_type,
            Questions.correct_answer,
            Responses.id.label("response_id"),
            Responses.user_id,
            Responses.iscorrect,
            Responses.answer,
        ).join(
            Questions, Questions.quiz_id == Quizzes.id
        ).join(
            Responses, Responses.question_id == Questions.id
        ).join(
            Users, Users.id == Responses.user_id
        ).filter(
            Quizzes.id == int(quiz_id)
        ).all()
        
        logger.info(quiz_results)
        dataFrame = pd.DataFrame(quiz_results)
        csv_string = dataFrame.to_csv(index=False)

        response = Response(content=csv_string)
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        response.headers["Content-Type"] = "text/csv"
        
        return response
    except HTTPException as http_error:
        raise http_error
    
    
    
@router.get(
    "/all_quizes",
    response_model=list[QuizData],
    status_code=status.HTTP_200_OK
)
def get_all_quizes(session: Session = Depends(get_db)):
    """_summary_

    Args:
        quiz_id (int): _description_
        session (Session, optional): _description_. Defaults to Depends(get_db).
    """
    try:
        all_quzzies = session.query(Quizzes).all()
        
        if not all_quzzies:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Quizzes Found")
        
        quiz_list = []
        for quiz in all_quzzies:
            formatted_date = quiz.created.strftime("%m-%d-%Y")
            quiz_list.append(QuizData(
                quiz_id=quiz.id,
                quiz_name=quiz.quiz_name,
                number_of_questions=quiz.number_of_questions,
                quiz_duration=quiz.quiz_duration,
                lecture_id=quiz.lecture_id,
                created_date=formatted_date
            ))
        logger.info(f"all quiz list: {quiz_list}")
            
        return quiz_list
    except HTTPException as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {error}")