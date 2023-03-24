from db_models import models
from db_models.set_session import LocalSession
from db_api.api_util import get_hashed_password

def create_admin_user(email, password, name):
    session = LocalSession()
    password = get_hashed_password(password)
    admin_user = models.Users(
        email=email,
        password=password,
        role=models.Role.INSTRUCTOR,
        name=name
    )
    session.add(admin_user)
    session.commit()


def create_class(class_name, course_code, instructor_id):
    session = LocalSession()
    new_class = models.Class(
        class_name=class_name,
        course_code=course_code,
        instructor_id=instructor_id,
        student_list=dict()
    )
    session.add(new_class)
    session.commit()
    

# create_admin_user("test@test.com", "Password", "OmarElsayd")

create_class("test3", "TEST333", 1)
    