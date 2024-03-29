#Author: Omar Elsayd
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql.base import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, and_
from sqlalchemy.orm import relationship
from db_models.base import Base


class Role(Enum):
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"
    TA = "TA"


class QuestionType(Enum):
    MultipleChoice = "Multiple Choice"
    TrueFalse = "True or False"
    ShortAnswer = "Short Answer"


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String)
    role = Column(ENUM(Role, name="role"))
    created = Column(DateTime, default=datetime.utcnow)
    
    
class Class(Base):
    __tablename__ = 'class'
    
    id = Column(Integer, primary_key=True)
    class_name = Column(String(50))
    course_code = Column(String(50))
    instructor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    student_list = Column(JSONB)
    
    user = relationship("Users")


class Lectures(Base):
    __tablename__ = 'lectures'
    
    id = Column(Integer, primary_key=True)
    lecture_name = Column(String)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    lecture_date = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created = Column(DateTime, default=datetime.utcnow)

    user = relationship("Users")
    class_ = relationship("Class")

    @classmethod
    def if_is_instructor(cls, session, lecture_id):
        with session.begin() as cls_session:
            instructor = cls_session.query(Users).filter(
                and_(Users.id == cls.instructor_id, Users.role == 'Instructor')
            ).first()
            if instructor:
                session.query(Lectures).filter(
                    Lectures.id == lecture_id).update({Lectures.is_instructor: True},
                                                      synchronize_session='evaluate')
            else:
                return


class Quizzes(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    quiz_name = Column(String(50))
    number_of_questions = Column(Integer)
    quiz_duration = Column(Integer)
    lecture_id = Column(ForeignKey('lectures.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    lectures = relationship('Lectures')
    questions = relationship('Questions', back_populates='quiz')


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question_order = Column(Integer)
    question_type = Column(ENUM(QuestionType, name="question_type"))
    question = Column(String(50))
    correct_answer = Column(String(50))
    quiz_id = Column(ForeignKey('quizzes.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    quiz = relationship('Quizzes', back_populates='questions')
    answers = relationship('QuestionAnswers', back_populates='question')


class QuestionAnswers(Base):
    __tablename__ = 'question_answers'

    id = Column(Integer, primary_key=True)
    answer = Column(String(50))
    question_id = Column(ForeignKey('questions.id'))

    question = relationship('Questions', back_populates='answers')


class Responses(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    question_id = Column(ForeignKey('questions.id'), nullable=False)
    quiz_id = Column(ForeignKey('quizzes.id'), nullable=False)
    answer = Column(String(50))
    iscorrect = Column(Boolean)
    created = Column(DateTime, default=datetime.utcnow)

    questions = relationship('Questions')
    users = relationship('Users')
    quizzes = relationship('Quizzes')


class Scores(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    quiz_id = Column(ForeignKey('quizzes.id'), nullable=False)
    score = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)

    quizzes = relationship('Quizzes')
    users = relationship('Users')

