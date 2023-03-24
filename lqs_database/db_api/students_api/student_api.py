from contextlib import contextmanager
import json
import logging

from db_api.instructor_apis.classes_util import WebSocketManager
from db_api.local_session import get_db, transaction
from fastapi import Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from typing import List
from sqlalchemy import delete
from .class_util import QuestionsResponces, QuizHeader, Quiz, Choice, Question
from sqlalchemy.orm import Session
from db_models.models import Class, Lectures, QuestionAnswers, QuestionType, Questions, Quizzes, Users, Role
from fastapi import APIRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}}
)

manager = WebSocketManager()

@router.get(
    "/get_quiz",
    status_code=status.HTTP_200_OK,
    response_model=Quiz
)
def get_quiz(
    quiz_code: str,
    session: Session = Depends(get_db)
    ):
    """
    
    """
    try:
        quiz = session.query(Quizzes).filter(Quizzes.quiz_name == quiz_code).first()
        lecture = session.query(Lectures).filter(Lectures.id == quiz.lecture_id).first()
        
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
        
        
        send_quiz = Quiz(
            questions=[],
            quiz_header=QuizHeader(
                quiz_duration=quiz.quiz_duration,
                number_of_questions=quiz.number_of_questions,
                class_code=quiz.quiz_name, 
                lecture_date=lecture.lecture_date,
                lecture_name=lecture.lecture_name
            )
        )
        
        questions = session.query(Questions).filter(Questions.quiz_id == quiz.id).all()
        
        for question in questions:
            
            question_answer = session.query(QuestionAnswers).filter(QuestionAnswers.question_id == question.id).all()
            
            if question.question_type.value == QuestionType.MultipleChoice.value:
                options = [answer.answer for answer in question_answer]
                send_quiz.questions.append(
                    QuestionsResponces(
                        question_order=question.question_order,
                        question_type=question.question_type.value,
                        question=question.question,
                        correct_answer=question.correct_answer,
                        option1=options[0],
                        option2=options[1],
                        option3=options[2],
                        option4=options[3]
                    )
                )
            else:
                send_quiz.questions.append(
                    QuestionsResponces(
                        question_order=question.question_order,
                        question_type=question.question_type.value,
                        question=question.question,
                        correct_answer=question.correct_answer,
                    )
                )
                
        
        return send_quiz
        
    except HTTPException:
        raise
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.websocket("/lobby_wait_ws")
async def lobby_wait_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            event = await websocket.receive_text()
            logger.info(f"Received event: {event}")
            if event == '"add_one"':
                logger.info(f"Received event: {event}")
                await manager.broadcast(json.dumps({'event': 'student_joined'}))
    except WebSocketDisconnect as e:
        logger.info(f"WebSocket disconnected with code: {e}")
    finally:
        await manager.disconnect(websocket)