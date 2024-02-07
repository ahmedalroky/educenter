from datetime import datetime
from typing import List, Optional

class School:
    """Represents an educational institution with basic details."""
    def __init__(self, school_id: int, name: str, address: str):
        self.school_id = school_id
        self.name = name
        self.address = address

class User:
    """Base class for all user types including common attributes."""
    def __init__(self, user_id: int, username: str, email: str, password: str, role: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password  # Passwords should be hashed
        self.role = role  # Role type (e.g., "student", "teacher", "admin")

class Profile:
    """Represents detailed profile information for a user."""
    def __init__(self, user: User, name: str, bio: Optional[str] = None):
        self.user = user
        self.name = name
        self.bio = bio

class Subject:
    """Defines a subject/course that can be taught in the school."""
    def __init__(self, subject_id: int, name: str, description: str):
        self.subject_id = subject_id
        self.name = name
        self.description = description

class ClassSession:
    """Represents a scheduled class session for a subject."""
    def __init__(self, class_id: int, subject: Subject, teacher: 'Teacher', day: str, time: datetime, location: str):
        self.class_id = class_id
        self.subject = subject
        self.teacher = teacher
        self.day = day
        self.time = time
        self.location = location

class Enrollment:
    """Manages the enrollment of a student in a specific class session."""
    def __init__(self, student: 'Student', class_session: ClassSession, enrollment_date: datetime):
        self.student = student
        self.class_session = class_session
        self.enrollment_date = enrollment_date

class Student(User):
    """Specialized User class for students, including academic details and enrollments."""
    def __init__(self, user_id: int, username: str, email: str, password: str, school: School, level: str, education_stage: str):
        super().__init__(user_id, username, email, password, "student")
        self.school = school
        self.level = level
        self.education_stage = education_stage
        self.enrollments = []  # List of Enrollment instances

    def enroll_in_class(self, class_session: ClassSession):
        """Method to enroll the student in a new class session."""
        enrollment = Enrollment(self, class_session, datetime.now())
        self.enrollments.append(enrollment)

class Teacher(User):
    """Specialized User class for teachers, including the classes they teach."""
    def __init__(self, user_id: int, username: str, email: str, password: str, school: School, level: str, education_stage: str):
        super().__init__(user_id, username, email, password, "teacher")
        self.school = school
        self.level = level
        self.education_stage = education_stage
        self.classes = []  # Classes the teacher is scheduled to teach

    def add_class(self, class_session: ClassSession):
        """Method to add a new class session to the teacher's schedule."""
        if class_session not in self.classes:
            self.classes.append(class_session)

class Admin(User):
    """Specialized User class for administrators with additional permissions."""
    def __init__(self, user_id: int, username: str, email: str, password: str, permissions: List[str]):
        super().__init__(user_id, username, email, password, "admin")
        self.permissions = permissions  # List of specific administrative permissions

class Notification:
    """Represents notifications sent to users within the app."""
    def __init__(self, notification_id: int, user: User, message: str, timestamp: datetime, read: bool = False):
        self.notification_id = notification_id
        self.user = user
        self.message = message
        self.timestamp = timestamp
        self.read = read

    def mark_as_read(self):
        """Marks the notification as read by the user."""
        self.read = True
