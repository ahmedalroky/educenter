from flask import Blueprint, jsonify, request
from app.models import db, Student

students_bp = Blueprint('students', __name__, url_prefix='/admin/students')

@students_bp.route('', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.serialize() for student in students])

@students_bp.route('', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(**data)
    db.session.add(student)
    db.session.commit()
    return jsonify(student.serialize()), 201

@students_bp.route('/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.serialize())

@students_bp.route('/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify(student.serialize())

@students_bp.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return '', 204
