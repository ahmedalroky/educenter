from .student import Student
from .class_session import ClassSession
from datetime import datetime

class Enrollment:
    def __init__(self, student: Student, class_session: ClassSession):
        self.student = student
        self.class_session = class_session
        self.enrollment_date = datetime.now()
