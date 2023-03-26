import datetime
from typing import List
from fastapi import WebSocket
from pydantic import BaseModel
from typing import Union


class Students(BaseModel):
    name: Union[str, None]
    email: Union[str, None]
    
    class Config:
        orm_mode = True
        
        
class genResponse(BaseModel):
    status: bool = False
    message: Union[str, None]
    
    class Config:
        orm_mode = True
        
class ClassInput(BaseModel):
    class_name: str
    course_code: str
    instructor_id: int
    
    class Config:
        orm_mode = True
        
class TaTemplete(BaseModel):
    name: str
    email: str
    password: str
    
    class Config:
        orm_mode = True
        
class CreateQuizResponse(BaseModel):
    status: bool = False
    message: Union[str, None]
    quiz_id: Union[int, None]
    quiz_code: Union[str, None]
    
    class Config:
        orm_mode = True
        
        
class CreateQuizInput(BaseModel):
    quiz_duration: float
    number_of_questions: int
    class_code: str
    lecture_name: str
    lecture_date: str
    
    class Config:
        orm_mode = True
        
class CreateQuestionInput(BaseModel):
    question: str
    question_type: str
    option1: Union[str, None]
    option2: Union[str, None]
    option3: Union[str, None]
    option4: Union[str, None]
    correct_answer: Union[str, None]

    class Config:
        orm_mode = True
        
class QuizData(BaseModel):
    quiz_id: int
    quiz_name: str
    number_of_questions: int
    quiz_duration: int
    lecture_id: int
    created_date: str
        
        
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)