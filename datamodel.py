from sqlalchemy import Column, Integer, String, Enum, Time, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Enrollment(Base):
    __tablename__ = 'enrollment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    enrollment_date = Column(Date)
    grade = Column(String(10))
    exam_score = Column(Integer)
    homework_score = Column(Integer)
    enrollment_type = Column(Enum('exam', 'homework'), nullable=False)

    student = relationship('Student', backref='enrollments')
    class_ = relationship('Class', backref='enrollments')


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    profile_picture = Column(String(255))
    phone_number = Column(String(20))
    school = Column(String(100))
    age = Column(Integer)
    grade = Column(String(20))
    email = Column(String(100), unique=True, nullable=False)
    speciality = Column(String(50))
    level = Column(String(20))
    password = Column(String(99),nullable=False)

    classes = relationship('Class', secondary='student_classes', back_populates='students')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    profile_picture = Column(String(255))
    phone_number = Column(String(20))
    school = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    location = Column(String(100))
    article = Column(String(255))
    grades = Column(String(255))
    level = Column(String(20))
    password = Column(String(99),nullable=False)

    classes = relationship('Class', back_populates='teacher')


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(100), nullable=False)
    day = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), nullable=False)
    time = Column(Time)
    location = Column(String(100))
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship('Teacher', back_populates='classes')
    students = relationship('Student', secondary='student_classes', back_populates='classes')


class StudentClass(Base):
    __tablename__ = 'student_classes'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
