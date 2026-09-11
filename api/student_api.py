class StudentAPI:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def add_student(self, name, age):
        return self.session.post(
            f"{self.base_url}/students",
            json={
                "name": name,
                "age": age
            }
        )

    def get_students(self):
        return self.session.get(
            f"{self.base_url}/students"
        )

    def get_student(self, student_id):
        return self.session.get(
            f"{self.base_url}/students/{student_id}"
        )

    def update_student(self, student_id, name, age):
        return self.session.put(
            f"{self.base_url}/students/{student_id}",
            json={
                "name": name,
                "age": age
            }
        )

    def delete_student(self, student_id):
        return self.session.delete(
            f"{self.base_url}/students/{student_id}"
        )