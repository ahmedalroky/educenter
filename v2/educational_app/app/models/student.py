from .user import User
from .school import School
from .enrollment import Enrollment  # Assuming you manage enrollments directly

class Student(User):
    def __init__(self, user_id: int, username: str, email: str, password: str, school: School, level: str, education_stage: str):
        super().__init__(user_id, username, email, password, "student")
        self.school = school
        self.level = level
        self.education_stage = education_stage
        self.enrollments = []  # Initialize as empty list

    # Additional student-specific methods here
