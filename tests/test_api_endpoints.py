def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "UP"

def test_students(client):
    response = client.get("/api/students")
    assert response.status_code == 200
    assert len(response.json["students"]) >= 1

def test_enroll_and_gpa(client):
    assert client.post("/api/enroll", json={"student_id":"S101","course_id":"C101"}).status_code == 201
    assert client.post("/api/grades", json={"student_id":"S101","course_id":"C101","grade":"A+"}).status_code == 201
    assert client.get("/api/gpa/S101").json["gpa"] == 9.0

def test_bad_grade(client):
    client.post("/api/enroll", json={"student_id":"S101","course_id":"C101"})
    assert client.post("/api/grades", json={"student_id":"S101","course_id":"C101","grade":"INVALID"}).status_code == 400
