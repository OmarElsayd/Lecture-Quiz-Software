from typing import List, Union
from pydantic import BaseModel


class Choice(BaseModel):
    text: str
    isCorrect: bool
    
class Question(BaseModel):
    type: str
    question: str
    choices: List[Choice] = None
    answer: str = None
    answerBoolean: bool = None
    
class QuizHeader(BaseModel):
    number_of_questions: int
    quiz_duration: int
    class_code: str
    lecture_name: str
    lecture_date: str
    
class QuestionsResponces(BaseModel):
    question_order: int
    question_type: str
    question: str
    correct_answer: Union[str, None]
    option1: str = None
    option2: str = None
    option3: str = None
    option4: str = None
    
class Quiz(BaseModel):
    quiz_header: QuizHeader
    questions: List[QuestionsResponces]