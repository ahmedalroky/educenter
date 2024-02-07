from .user import User
from .school import School
from .class_session import ClassSession  # Assuming you want to reference class sessions

class Teacher(User):
    def __init__(self, user_id: int, username: str, email: str, password: str, school: School, level: str, education_stage: str):
        super().__init__(user_id, username, email, password, "teacher")
        self.school = school
        self.level = level
        self.education_stage = education_stage
        self.classes = []  # Initialize as empty list

    # Methods to add or manage class sessions
