from database.db import db

MAX_CREDITS = 18
GRADE_POINTS = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0}

class AcademicService:
    @staticmethod
    def add_student(student_id, name, department):
        if not all([student_id, name, department]):
            raise ValueError("All student fields are required")
        with db.lock:
            if student_id in db.students:
                raise ValueError("Student already exists")
            record = {"student_id": student_id, "name": name, "department": department}
            db.students[student_id] = record
            return record

    @staticmethod
    def enroll(student_id, course_id):
        with db.lock:
            if student_id not in db.students or course_id not in db.courses:
                raise ValueError("Invalid student or course")
            active = db.enrollments.setdefault(student_id, [])
            if course_id in active:
                raise ValueError("Enrollment conflict: already enrolled")
            used = sum(db.courses[c]["credits"] for c in active)
            if used + db.courses[course_id]["credits"] > MAX_CREDITS:
                raise ValueError("Credit limit exceeded (18 per semester)")
            active.append(course_id)
            return {"student_id": student_id, "course_id": course_id, "total_credits": used + db.courses[course_id]["credits"]}

    @staticmethod
    def add_grade(student_id, course_id, grade):
        if grade not in GRADE_POINTS:
            raise ValueError("Unknown grade")
        with db.lock:
            if course_id not in db.enrollments.get(student_id, []):
                raise ValueError("Student is not enrolled in this course")
            db.grades[(student_id, course_id)] = grade
            return {"student_id": student_id, "course_id": course_id, "grade": grade}

    @staticmethod
    def calculate_gpa(student_id):
        with db.lock:
            if student_id not in db.students:
                raise ValueError("Student not found")
            grade_pairs = [(c, db.grades[(student_id, c)]) for c in db.enrollments.get(student_id, []) if (student_id, c) in db.grades]
            credits = sum(db.courses[c]["credits"] for c, _ in grade_pairs)
            gpa = round(sum(db.courses[c]["credits"] * GRADE_POINTS[g] for c, g in grade_pairs) / credits, 2) if credits else 0.0
            return {"student_id": student_id, "graded_credits": credits, "gpa": gpa}
