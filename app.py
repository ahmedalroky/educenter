from flask import Flask, jsonify, request
import os
from werkzeug.exceptions import HTTPException
import datetime
from datetime import  timedelta
from flask_jwt_extended import JWTManager,jwt_required, get_jwt,create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datamodel import Base, Student, Teacher, Class, StudentClass, Admin, Enrollment
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.orm import class_mapper

import re
# create the database engine
engine = create_engine('mysql+pymysql://root@localhost/educenter')

# create the database tables
Base.metadata.create_all(engine)

# create a session
Session = sessionmaker(bind=engine)
session = Session()

# create a Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads/'
JWT_EXPIRATION_DELTA = datetime.timedelta(days=30)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

jwt = JWTManager(app)
def allowed_file(filename):
    """Check if a file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response = jsonify({
        'code': error.code,
        'name': error.name,
        'description': error.description,
    })
    response.status_code = error.code
    return response

@app.errorhandler(404)
def handle_not_found(error):
    response = jsonify({
        'code': 404,
        'name': 'Not Found',
        'description': 'The requested resource could not be found.',
    })
    response.status_code = 404
    return response


# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     # handle HTTP exceptions
#     response = e.get_response()
#     response.data = jsonify({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description
#     })
#     response.content_type = "application/json"
#     return response

# @app.errorhandler(Exception)
# def handle_exception(e):
#     # handle other exceptions
#     response = jsonify({
#         "code": 500,
#         "name": "Internal Server Error",
#         "description": "An unexpected error occurred."
#     })
#     response.status_code = 500
#     return response

#get all inrollments
@app.route('/enrollments', methods=['GET'])
@jwt_required()
def get_all_enrollments():
    current_user_id = get_jwt()["sub"]['user_id']
    current_user_role = get_jwt()["sub"]['user_type']
    if current_user_role == "admin":
        # retrieve all enrollments
        enrollments = session.query(Enrollment).all()
    elif current_user_role == "teacher":
        teacher_id = get_jwt()["sub"]['user_id']
        # retrieve enrollments for teacher's classes
        teacher_classes = session.query(Class.id).filter_by(teacher_id=teacher_id).all()
        teacher_class_ids = [c[0] for c in teacher_classes]
        enrollments = session.query(Enrollment).filter(Enrollment.class_id.in_(teacher_class_ids)).all()
    elif current_user_role == "student":
        student_id = get_jwt()["sub"]['user_id']
        # retrieve enrollments for teacher's classes
        enrollments = session.query(Enrollment).filter_by(student_id=student_id).all()

    else :
        return jsonify({'message': 'Unauthorized access'}), 401
    
    # check for class_id and student_id query parameters
    class_id = request.args.get('class_id')
    student_id = request.args.get('student_id')
    if class_id:
        enrollments = [e for e in enrollments if e.class_id == int(class_id)]
    if student_id:
        enrollments = [e for e in enrollments if e.student_id == int(student_id)]

    # create a list to store the enrollment data
    enrollment_list = []
    # iterate over the enrollments and add their data to the list
    for enrollment in enrollments:
        enrollment_data = {
            'id': enrollment.id,
            'student_id': enrollment.student_id,
            'class_id': enrollment.class_id,
            'enrollment_date': str(enrollment.enrollment_date), # need to convert date object to string for JSON serialization
            'grade': enrollment.grade,
            'exam_score': enrollment.exam_score,
            'homework_score': enrollment.homework_score,
            'enrollment_type': enrollment.enrollment_type,
            'student': {
                'id': enrollment.student.id,
                'name': enrollment.student.name,
                'email': enrollment.student.email
            },
            'class': {
                'id': enrollment.class_.id,
                'subject': enrollment.class_.subject,
                'day': enrollment.class_.day,
                'time': str(enrollment.class_.time), # need to convert time object to string for JSON serialization
                'location': enrollment.class_.location,
                'teacher': {
                    'id': enrollment.class_.teacher.id,
                    'name': enrollment.class_.teacher.name,
                    'email': enrollment.class_.teacher.email
                }
            }
        }
        enrollment_list.append(enrollment_data)
    # return the enrollment list as JSON
    return jsonify(enrollment_list)

@app.route('/enrollments/add', methods=['POST'])
@jwt_required()
def add_enrollment():
    current_user_id = get_jwt()["sub"]['user_id']
    current_user_role = get_jwt()["sub"]['user_type']
    
    if current_user_role != "teacher":
        return jsonify({'message': 'Unauthorized access'}), 401
    
    # retrieve student_id, class_id, enrollment_date, grade, exam_score, homework_score, enrollment_type from request body
    student_id = request.json.get('student_id', None)
    class_id = request.json.get('class_id', None)
    enrollment_date = request.json.get('enrollment_date', None)
    grade = request.json.get('grade', None)
    exam_score = request.json.get('exam_score', None)
    homework_score = request.json.get('homework_score', None)
    enrollment_type = request.json.get('enrollment_type', None)
    
    # check if all required fields are provided
    if not student_id or not class_id or not enrollment_date or not enrollment_type:
        return jsonify({'message': 'Student id, class id, enrollment date and enrollment type are required fields'}), 400
    
    try:
        # create new enrollment object and add to session
        enrollment = Enrollment(student_id=student_id, class_id=class_id, enrollment_date=enrollment_date, grade=grade, exam_score=exam_score, homework_score=homework_score, enrollment_type=enrollment_type)
        session.add(enrollment)
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Failed to add enrollment. Error: {}'.format(str(e))}), 500
    
    return jsonify({'message': 'Enrollment added successfully'}), 201

@app.route('/enrollments/<int:id>', methods=['PUT'])
@jwt_required()
def update_enrollment(id):
    current_user_id = get_jwt()["sub"]['user_id']
    current_user_role = get_jwt()["sub"]['user_type']
    
    if current_user_role != "teacher":
        return jsonify({'message': 'Unauthorized access'}), 401
    
    # retrieve enrollment object to be updated
    enrollment = session.query(Enrollment).filter_by(id=id).first()
    if not enrollment:
        return jsonify({'message': 'Enrollment not found'}), 404
    
    # retrieve updated enrollment data from request body
    enrollment_date = request.json.get('enrollment_date', None)
    grade = request.json.get('grade', None)
    exam_score = request.json.get('exam_score', None)
    homework_score = request.json.get('homework_score', None)
    enrollment_type = request.json.get('enrollment_type', None)
    
    # update enrollment object and commit changes
    enrollment.enrollment_date = enrollment_date if enrollment_date else enrollment.enrollment_date
    enrollment.grade = grade if grade else enrollment.grade
    enrollment.exam_score = exam_score if exam_score else enrollment.exam_score
    enrollment.homework_score = homework_score if homework_score else enrollment.homework_score
    enrollment.enrollment_type = enrollment_type if enrollment_type else enrollment.enrollment_type
    session.commit()
    
    return jsonify({'message': 'Enrollment updated successfully'}), 200



#image upload
@app.route('/upload/image', methods=['POST'])
@jwt_required()
def upload_image():
    # get the current user's role and id
    current_user_role = get_jwt()["sub"]['user_type']
    current_user_id = get_jwt()["sub"]['user_id']
    
    # check if authenticated user is allowed to upload images
    if current_user_role != "admin" and current_user_role != "teacher" and current_user_role != "student":
        return jsonify({'message': 'Unauthorized access'}), 401

    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    # check if the file is empty
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    # check if the file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({'message': 'Invalid file extension. Allowed extensions are ' + ', '.join(ALLOWED_EXTENSIONS)}), 400

    # determine the upload directory based on the user type
    upload_dir = app.config['UPLOAD_FOLDER']

    # create the upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)

    # save the file to the upload directory with the user id as the filename
    filename = secure_filename(str(current_user_role[0]) + str(current_user_id) + "." + file.filename.rsplit('.', 1)[1])
    file.save(os.path.join(upload_dir, filename))
    
    return jsonify({'message': 'File uploaded successfully'}), 200

#add admin
@app.route('/admin/add', methods=['POST'])
@jwt_required()
def add_admin():
    # check if authenticated user is an admin
    current_user_id = get_jwt()["sub"]['user_id']
    current_user_role = get_jwt()["sub"]['user_type']
    if (current_user_role != "admin"):
        return jsonify({'message': 'Unauthorized access'}), 401

    # retrieve data from request body
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    # create new admin object and add it to database
    admin = Admin(name=name, email=email, password=password)
    session = Session()
    session.add(admin)
    try : 
        session.commit()
    except:
        return jsonify({'message': 'Email already exists'}), 409

    return jsonify({'message': 'Admin added successfully'}), 201



#admin login route
@app.route('/admin/login', methods=['POST'])
def login_admin():
    # retrieve email and password from request body
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    # check if email and password are provided
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    # check if admin exists and password is valid
    session = Session()
    admin = session.query(Admin).filter_by(email=email).first()
    if not admin or admin.password != password:
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # create JWT token
    jwt_payload = {
        'sub': admin.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'user_id': admin.id,
        'user_type': 'admin'
    }
    jwt_token = create_access_token(identity=jwt_payload)
    
    return jsonify({'access_token': jwt_token}), 200

# route to get all classes
@app.route('/classes', methods=['GET'])
@jwt_required()
def get_all_classes():
    current_user_id = get_jwt()["sub"]['user_id']
    print(current_user_id)
    current_user_role = get_jwt()["sub"]['user_type']
    if (current_user_role!="admin"):
        return jsonify({'message': 'Unauthorized access'}), 401
    elif current_user_role=="admin":
        pass
    # retrieve all classes
    classes = session.query(Class).all()
    # create a list to store the class data
    class_list = []
    # iterate over the classes and add their data to the list
    for class_ in classes:
        class_data = {
            'id': class_.id,
            'subject': class_.subject,
            'day': class_.day,
            'time': str(class_.time), # need to convert time object to string for JSON serialization
            'location': class_.location,
            'teacher': {
                'id': class_.teacher.id,
                'name': class_.teacher.name,
                'email': class_.teacher.email
            }
        }
        class_list.append(class_data)
    # return the class list as JSON
    return jsonify(class_list)

#student signup
@app.route('/students/signup', methods=['POST'])
def signup():
        # get the data from the request
    # Add this at the beginning of the signup route
    name = request.json.get('name', '').strip()
    email = request.json.get('email', '').strip()
    password = request.json.get('password', '').strip()
    phone_number = request.json.get('phone_number', '').strip()
    # Check if any of the required fields are empty
    if not name or not email or not password or not phone_number:
        return jsonify(message='Name, email, phone_number, and password are required'), 400

    # Check if the email is a valid email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(message='Invalid email format'), 400

    # Check if the password meets the minimum requirements
    if len(password) < 8:
        return jsonify(message='Password must be at least 8 characters'), 400
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    phone_number = request.json.get('phone_number')
    school = request.json.get('school')
    age = request.json.get('age')
    grade = request.json.get('grade')
    speciality = request.json.get('speciality')
    birthday = request.json.get('birthday')

    # check if the user already exists
    student = session.query(Student).filter_by(email=email).first()
    if student:
        return jsonify({'message': 'Email already exists'}), 409

    # create a new student instance
    new_student = Student(
        name=name,
        email=email,
        password=password,
        phone_number=phone_number,
        school=school,
        age=age,
        grade=grade,
        speciality=speciality,
        birthday=birthday
    )

    # add the student to the database
    session.add(new_student)
    session.commit()

    # return the student information as JSON with a success message
    return jsonify({
        'message': 'Student created successfully',
        'student': {
            'id': new_student.id,
            'name': new_student.name,
            'email': new_student.email,
            'phone_number': new_student.phone_number,
            'school': new_student.school,
            'age': new_student.age,
            'grade': new_student.grade,
            'speciality': new_student.speciality,
            'birthday':new_student.birthday
        }
    }), 201

#student login

@app.route('/students/login', methods=['POST'])
def login_student():
    # retrieve email and password from request body
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    # check if email and password are provided
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    # check if student exists and password is valid
    session = Session()
    student = session.query(Student).filter_by(email=email).first()
    if not student or student.password != password:
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # create JWT token
    jwt_payload = {
        'sub': student.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'user_id': student.id,
        'user_type': 'student'
    }
    jwt_token = create_access_token(identity=jwt_payload)
    
    return jsonify({'access_token': jwt_token}), 200


# route to get all students
@app.route('/students', methods=['GET'])
@jwt_required()
def get_all_students():
    current_user_id = get_jwt()["sub"]['user_id']
    print(current_user_id)
    current_user_role = get_jwt()["sub"]['user_type']
    if (current_user_role!="admin"):
        return jsonify({'message': 'Unauthorized access'}), 401
    elif current_user_role=="admin":
        pass
    # retrieve all students
    students = session.query(Student).all()
    # create a list to store the student data
    student_list = []
    # iterate over the students and add their data to the list
    for student in students:
        student_data = {
            'id': student.id,
            'name': student.name,
            'profile_picture': student.profile_picture,
            'phone_number': student.phone_number,
            'school': student.school,
            'age': student.age,
            'grade': student.grade,
            'email': student.email,
            'speciality': student.speciality,
            'level': student.level
        }
        student_list.append(student_data)
    # return the student list as JSON
    return jsonify(student_list)

@app.route('/students/<int:student_id>')
@jwt_required()
def get_student_profile(student_id):
    current_user_id = get_jwt()["sub"]['user_id']
    print(current_user_id)
    current_user_role = get_jwt()["sub"]['user_type']
    if (current_user_id != student_id or current_user_role!="student") and (current_user_role!="admin"):
        return jsonify({'message': 'Unauthorized access'}), 401
    elif current_user_role=="admin":
        pass
    elif current_user_role=="teacher":
        pass
    # retrieve the student by id
    student = session.query(Student).filter_by(id=student_id).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    # create a dictionary with the student information
    student_dict = {
        'id': student.id,
        'name': student.name,
        'profile_picture': student.profile_picture,
        'phone_number': student.phone_number,
        'school': student.school,
        'age': student.age,
        'grade': student.grade,
        'email': student.email,
        'speciality': student.speciality,
        'level': student.level
    } 
    # return the student information as a JSON response
    return jsonify(student_dict)

@app.route('/students/<int:student_id>/classes')
@jwt_required()
def get_classes_for_student(student_id):
    current_user_id = get_jwt()["sub"]['user_id']
    print(current_user_id)
    current_user_role = get_jwt()["sub"]['user_type']
    if (current_user_id != student_id or current_user_role!="student") and (current_user_role!="admin"):
        return jsonify({'message': 'Unauthorized access'}), 401
    elif current_user_role=="admin":
        pass
    # elif current_user_role=="teacher":
    #     pass
    # get the student by id
    student = session.query(Student).filter_by(id=student_id).first()

    # get all the classes for the student
    classes = session.query(Class).join(StudentClass).filter_by(student_id=student_id).all()

    # convert the classes to a list of dictionaries
    classes_dict = []
    for class_ in classes:
        classes_dict.append({
            'subject': class_.subject,
            'day': class_.day,
            'time': class_.time.strftime('%H:%M:%S'),
            'location': class_.location,
            'teacher': class_.teacher.name
        })

    # return the classes as JSON
    return jsonify({
        'student_name': student.name,
        'classes': classes_dict
    })

#teacher login
@app.route('/teachers/login', methods=['POST'])
def login_teacher():
    # retrieve email and password from request body
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    # check if email and password are provided
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    # check if teacher exists and password is valid
    session = Session()
    teacher = session.query(Teacher).filter_by(email=email).first()
    if not teacher or teacher.password != password:
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # create JWT token
    jwt_payload = {
        'sub': teacher.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'user_id': teacher.id,
        'user_type': 'teacher'
    }
    jwt_token = create_access_token(identity=jwt_payload)
    
    return jsonify({'access_token': jwt_token}), 200

#add teacher
@app.route('/teachers/add', methods=['POST'])
@jwt_required()
def add_teacher():
    # check if authenticated user is an admin
    current_user_id = get_jwt()["sub"]['user_id']
    current_user_role = get_jwt()["sub"]['user_type']
    if (current_user_role != "admin"):
        return jsonify({'message': 'Unauthorized access'}), 401

    # retrieve data from request body
    name = request.json.get('name')
    profile_picture = request.json.get('profile_picture')
    phone_number = request.json.get('phone_number')
    school = request.json.get('school')
    email = request.json.get('email')
    location = request.json.get('location')
    article = request.json.get('article')
    grades = request.json.get('grades')
    level = request.json.get('level')

    # create new teacher object and add it to database
    teacher = Teacher(
        name=name,
        profile_picture=profile_picture,
        phone_number=phone_number,
        school=school,
        email=email,
        location=location,
        article=article,
        grades=grades,
        level=level
    )
    session.add(teacher)
    try:
        session.commit()
    except :
        session.rollback()
        return jsonify({'message': 'Email already exists'}), 409

    return jsonify({'message': 'Teacher added successfully'}), 201

# route to get all teachers
@app.route('/teachers', methods=['GET'])
def get_all_teachers():
    # retrieve all teachers
    teachers = session.query(Teacher).all()
    # create a list to store the teacher data
    teacher_list = []
    # iterate over the teachers and add their data to the list
    for teacher in teachers:
        teacher_data = {
            'id': teacher.id,
            'name': teacher.name,
            'profile_picture': teacher.profile_picture,
            'phone_number': teacher.phone_number,
            'school': teacher.school,
            'email': teacher.email,
            'location': teacher.location,
            'article': teacher.article,
            'grades': teacher.grades,
            'level': teacher.level
        }
        teacher_list.append(teacher_data)
    # return the teacher list as JSON
    return jsonify(teacher_list)

@app.route('/teachers/<int:teacher_id>')
def get_teacher_profile(teacher_id):
    # query the teacher by their ID
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()

    # if the teacher doesn't exist, return a 404 error
    if not teacher:
        return jsonify({'error': 'Teacher not found.'}), 404

    # create a dictionary of the teacher's profile information
    teacher_profile = {
        'id': teacher.id,
        'name': teacher.name,
        'email': teacher.email,
        'location': teacher.location,
        'article': teacher.article,
        'grades': teacher.grades,
        'level': teacher.level
    }

    # return the teacher's profile as JSON
    return jsonify(teacher_profile)
# define an endpoint to get all classes for a teacher
@app.route('/teachers/<int:teacher_id>/classes')
@jwt_required()
def get_classes_for_teacher(teacher_id):
    current_user_id = get_jwt()["sub"]['user_id']
    print(current_user_id)
    current_user_role = get_jwt()["sub"]['user_type']
    if (current_user_id != teacher_id or current_user_role!="teacher") and (current_user_role!="admin"):
        return jsonify({'message': 'Unauthorized access'}), 401
    elif current_user_role=="admin":
        pass
    # retrieve the teacher by id
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404
    # retrieve the teacher by id
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404
    # get the teacher by id


    teacher = session.query(Teacher).filter_by(id=teacher_id).first()

    # get all classes for the teacher
    classes = session.query(Class).filter(Class.teacher == teacher).all()

    # convert the classes to a list of dictionaries
    classes_dict = []
    for class_ in classes:
        classes_dict.append({
            'id': class_.id,
            'subject': class_.subject,
            'day': class_.day,
            'time': class_.time.strftime('%H:%M:%S'),
            'location': class_.location
        })

    # return the classes as JSON
    return jsonify({
        'teacher_name': teacher.name,
        'classes': classes_dict
    })

if __name__ == '__main__':
    app.run(debug=False)
