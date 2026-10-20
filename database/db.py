import threading

class Database:
    def __init__(self):
        self.lock = threading.RLock()
        self.reset()

    def reset(self):
        with self.lock:
            self.students = {"S101": {"student_id": "S101", "name": "Om Laware", "department": "AI & Data Science"}}
            self.courses = {"C101": {"course_id": "C101", "name": "Python Programming", "credits": 4},
                            "C102": {"course_id": "C102", "name": "Data Structures", "credits": 4},
                            "C103": {"course_id": "C103", "name": "Statistics", "credits": 3}}
            self.enrollments = {}
            self.grades = {}

db = Database()
