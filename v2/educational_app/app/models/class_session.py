from .subject import Subject
from .teacher import Teacher

class ClassSession:
    def __init__(self, class_id: int, subject: Subject, teacher: Teacher, day: str, time: str, location: str):
        self.class_id = class_id
        self.subject = subject
        self.teacher = teacher
        self.day = day
        self.time = time
        self.location = location
