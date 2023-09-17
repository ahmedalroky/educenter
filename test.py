from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import time
from datamodel import Base, Student, Teacher, Class, StudentClass

# create the database engine
engine = create_engine('mysql+pymysql://root@localhost/educenter')

# create the database tables
Base.metadata.create_all(engine)

# create a session
Session = sessionmaker(bind=engine)
session = Session()


# add a student to a class
#student_class = StudentClass(student=student, class_=class_)
#session.add(student_class)
#session.commit()
print("students \n")
# retrieve all students
students = session.query(Student).all()
for student in students:
    print(student.name, student.email)

# retrieve all teachers
print("teachers \n")
teachers = session.query(Teacher).all()
for teacher in teachers:
    print(teacher.name, teacher.email)

# retrieve all classes
print("classes \n")
classes = session.query(Class).all()
for class_ in classes:
    print(class_.subject, class_.day, class_.time, class_.location, class_.teacher.name)

print("\n")

# get the student by id
student_id = 1
student = session.query(Student).filter_by(id=student_id).first()

# get all the classes for the student
classes = session.query(Class).join(StudentClass).filter_by(student_id=student_id).all()

# print the classes for the student
print(f"Classes for {student.name}:")
for class_ in classes:
    print(class_.subject)

print("\n")

teacher_id = 1  # example id
teacher = session.query(Teacher).filter_by(id=teacher_id).first()

# get all classes for the teacher
classes = session.query(Class).filter(Class.teacher == teacher).all()
print(f"Classes for {teacher.name}:")
# print the class information
for c in classes:
    print(f"Class ID: {c.id}, Subject: {c.subject}, Day: {c.day}, Time: {c.time}, Location: {c.location}")