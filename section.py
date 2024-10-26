from mongoengine import *
import mongoengine
from course import Course
from enrollment import Enrollment
from datetime import datetime
class Section(Document):
    department_abbreviation = StringField(max_length=6, required=True)
    course_name = StringField(max_length=100, required=True)
    course_number = IntField(min_value=100, max_value=699, required=True)
    section_number = IntField(required=True)
    semester = StringField(choices=['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'], required=True)
    section_year = IntField(required=True)
    building = StringField(choices=['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                           required=True)
    room = IntField(min_value=1, max_value=999, required=True)
    schedule = StringField(choices=['MW', 'TuTh', 'MWF', 'F', 'S'], required=True)
    start_time = DateTimeField(required=True)
    instructor = StringField(required=True)
    enrollments = ListField(ReferenceField('Enrollment'))

    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['course_name','section_number', 'section_year', 'semester'],
                 'name': 'sections_uk_1'},
                {'unique': True, 'fields': ['semester', 'section_year', 'building', 'room','schedule', 'start_time'],
                 'name': 'sections_uk_2'},
                {'unique': True, 'fields': ['semester', 'section_year', 'schedule', 'start_time','instructor'],
                 'name': 'sections_uk_3'}
            ]}

    def __init__(self, department_abbreviation:str,course_name:str,course_number:int,section_number:int, semester:str, section_year:int, building:str,
                 room:int, schedule:str, start_time:datetime.time, instructor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department_abbreviation = department_abbreviation
        self.course_name = course_name
        self.course_number = course_number
        self.section_number = section_number
        self.semester = semester
        self.section_year = section_year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.start_time = start_time
        self.instructor = instructor
        if self.enrollments is None:
            self.enrollments = []

    def __str__(self):
        results = (f"Section:Department:{self.department_abbreviation}, Course name: {self.course_name},Course number: {self.course_number} Section number: {self.section_number}, Semester:{self.semester} {self.section_year}\n"
                f"Building: {self.building}, Room {self.room}, Schedule: {self.schedule} {self.start_time}, Instructor: {self.instructor}\n")
        for x in self.enrollments:
            student = x.student_id
            results = results + '\n' + f'Enrollments: {student}'
        return results

    def add_enrollment(self, enrollment):
        self.enrollments.append(enrollment)

    def remove_enrollment(self, enrollment):
        self.enrollments.remove(enrollment)