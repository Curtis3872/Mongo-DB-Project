from mongoengine import *
import mongoengine
from department import Department
from student_major import StudentMajor
class Major(Document):
    department = ObjectIdField(required=True)
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=800, required=True)
    students = ListField(EmbeddedDocumentField(StudentMajor), db_field='students')

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'majors_uk_1'},
                {'unique': True, 'fields': ['description'], 'name': 'majors_uk_2'}
            ]}

    def __init__(self,department:Department, name, description, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.name = name
        self.description = description
        if self.students is None:
            self.students = []

    def __str__(self):
        results = f"Major: {self.name}\nDescription: {self.description} "
        for x in self.students:
            enrolled_student = f"\nStudentID: {x.student_id}"
            results = results + enrolled_student
        return results


    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        self.students.remove(student)