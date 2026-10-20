import pytest
from database.db import db
from app.services.academic_service import AcademicService

def test_student_creation():
    db.reset()
    s = AcademicService.add_student("S200", "Test Student", "AIDS")
    assert s["name"] == "Test Student"

def test_conflict_prevention():
    db.reset()
    AcademicService.enroll("S101", "C101")
    with pytest.raises(ValueError, match="conflict"):
        AcademicService.enroll("S101", "C101")

def test_weighted_gpa():
    db.reset()
    AcademicService.enroll("S101", "C101")
    AcademicService.enroll("S101", "C102")
    AcademicService.add_grade("S101", "C101", "O")
    AcademicService.add_grade("S101", "C102", "A")
    assert AcademicService.calculate_gpa("S101")["gpa"] == 9.0

def test_credit_limit():
    db.reset()
    with db.lock:
        for i in range(4, 9):
            db.courses[f"C{i}"] = {"course_id": f"C{i}", "name": str(i), "credits": 4}
    for i in range(4, 8):
        AcademicService.enroll("S101", f"C{i}")
    with pytest.raises(ValueError, match="Credit limit"):
        AcademicService.enroll("S101", "C8")
