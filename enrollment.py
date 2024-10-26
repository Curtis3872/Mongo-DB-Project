from mongoengine import *

class Enrollment(Document):
    student_id = ObjectIdField(required=True)
    department_abbreviation = StringField(max_length=6, required=True)
    course_name = StringField(max_length=100, required=True)
    course_number = IntField(required=True)
    section_number = IntField(required=True)
    semester = StringField(required=True)
    section_year = IntField(required=True)

    meta = {'collection': 'enrollments','allow_inheritance': True,
            'indexes': [
                {'unique': True, 'fields': ['student_id', 'section_number', 'semester', 'department_abbreviation', 'course_number'], 'name': 'enrollments_uk_1'}
            ]}

    def __init__(self, student_id, department_abbreviation,course_name,course_number, section_number, semester,  section_year,*args, **values):
        super().__init__(*args, **values)
        self.student_id = student_id
        self.department_abbreviation = department_abbreviation
        self.course_name = course_name
        self.course_number = course_number
        self.section_number = section_number
        self.semester = semester
        self.section_year = section_year

    def __str__(self):
        return (f"Enrollment: Student ID - {self.student_id}, Department:{self.department_abbreviation}, Course number: {self.course_number}, "
                f"Section Number - {self.section_number}, Semester - {self.semester}, Section Year - {self.section_year}")

