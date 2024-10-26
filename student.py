from mongoengine import *
from student_major import StudentMajor
from enrollment import Enrollment
class Student(Document):
    last_name = StringField(max_length=100, required=True)
    first_name = StringField(max_length=100, required=True)
    email = EmailField(required=True)
    majors = ListField(EmbeddedDocumentField(StudentMajor), db_field='majors')
    enrollments = ListField(ReferenceField('Enrollment'))

    meta = {'collection': 'students',
            'indexes': [
                {'unique': True, 'fields': ['email'], 'name': 'students_uk_1'},
                {'unique': True, 'fields': ['last_name', 'first_name'], 'name': 'students_uk_2'}
            ]}
    def __init__(self, last_name, first_name, email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        if self.enrollments is None:
            self.enrollments = []
        if self.majors is None:
            self.majors = []

    def __str__(self):
        results =  f"Student: {self.first_name} {self.last_name}\nEmail: {self.email}\n"
        for x in self.enrollments:
            section = f"Course: {x.course_name} {x.course_number}, Section: {x.section_number}"
            results = results + section
        return  results

    def add_majors(self, major):
        self.majors.append(major)

    def remove_majors(self, major):
        self.majors.remove(major)

    def add_enrollment(self, enrollment):
        self.enrollments.append(enrollment)

    def remove_enrollment(self, enrollment):
        self.enrollments.remove(enrollment)