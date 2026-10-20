from flask import Blueprint, jsonify, request
from app.services.academic_service import AcademicService
from database.db import db

api_bp = Blueprint("api", __name__)

@api_bp.get("/health")
def health():
    return jsonify(status="UP", service="Student Academic Platform", version="1.0.0")

@api_bp.get("/students")
def students():
    with db.lock:
        return jsonify(students=list(db.students.values()))

@api_bp.post("/students")
def create_student():
    data = request.get_json(silent=True) or {}
    try:
        record = AcademicService.add_student(data.get("student_id"), data.get("name"), data.get("department"))
        return jsonify(record), 201
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

@api_bp.get("/courses")
def courses():
    with db.lock:
        return jsonify(courses=list(db.courses.values()))

@api_bp.post("/enroll")
def enroll():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(AcademicService.enroll(data.get("student_id"), data.get("course_id"))), 201
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

@api_bp.post("/grades")
def grades():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(AcademicService.add_grade(data.get("student_id"), data.get("course_id"), data.get("grade"))), 201
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

@api_bp.get("/gpa/<student_id>")
def gpa(student_id):
    try:
        return jsonify(AcademicService.calculate_gpa(student_id))
    except ValueError as exc:
        return jsonify(error=str(exc)), 404
