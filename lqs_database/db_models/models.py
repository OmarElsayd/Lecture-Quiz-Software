from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql.base import ENUM
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, and_
from sqlalchemy.orm import relationship
from lqs_database.db_models.base import Base


class Role(Enum):
    Instructor = "Instructor"
    Student = "Student"
    TA = "TA"


class QuizType(Enum):
    MultipleChoice = "Multiple Choice"


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    role = Column(ENUM(Role))
    created = Column(DateTime, default=datetime.utcnow)


class Lectures(Base):
    __tablename__ = 'lectures'
    id = Column(Integer, primary_key=True)
    lecture_name = Column(String)
    lecture_date = Column(String)
    user_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'), nullable=True)
    is_instructor = Column(Boolean, unique=False, default=False)
    number_of_students = Column(Integer)
    user = relationship("Users", back_populates="lectures")
    created = Column(DateTime, default=datetime.utcnow)

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
    quiz_type = Column(ENUM(QuizType))
    number_of_questions = Column(Integer)
    quiz_duration = Column(Integer)
    lecture_id = Column(ForeignKey('lectures.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    lectures = relationship('Lectures')


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String(50))
    correct_answer = Column(String(50))
    answer_list_id = Column(ForeignKey('answer_lists.id'), nullable=False)
    quiz_id = Column(ForeignKey('quizzes.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    answer_lists = relationship('AnswerLists')
    quizzes = relationship('Quizzes')


class AnswerLists(Base):
    __tablename__ = 'answer_lists'

    id = Column(Integer, primary_key=True)
    first_answer = Column(String(50))
    second_answer = Column(String(50))
    third_answer = Column(String(50))
    fourth_answer = Column(String(50))
    created = Column(DateTime, default=datetime.utcnow)


class Responses(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    question_id = Column(ForeignKey('questions.id'), nullable=False)
    answer = Column(String(50))
    correct = Column(Boolean)
    created = Column(DateTime, default=datetime.utcnow)

    questions = relationship('Questions')
    users = relationship('Users')


class Scores(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    quiz_id = Column(ForeignKey('quizzes.id'), nullable=False)
    score = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)

    quizzes = relationship('Quizzes')
    users = relationship('Users')

