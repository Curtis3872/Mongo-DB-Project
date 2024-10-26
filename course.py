import mongoengine
from mongoengine import *
from department import Department
class Course(Document):
    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    department_abbreviation = StringField(max_length=6, required=True)
    course_name = StringField(max_length=100, required=True)
    course_number = IntField(min_value=100, max_value=699, required=True)
    units = IntField(min_value=1, max_value=5, required=True)
    description = StringField(max_length=800, required=True)
    sections = ListField(ReferenceField('Section'))

    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['department_abbreviation','course_number'], 'name': 'courses_uk_1'},
                {'unique': True, 'fields': ['department_abbreviation','course_name'], 'name': 'courses_uk_2'}
            ]}

    def __init__(self, department:Department,department_abbreviation:str,course_name: str, course_number: str, units:int, description:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.department_abbreviation = department_abbreviation
        self.course_name = course_name
        self.course_number = course_number
        self.description = description
        self.units = units
        if self.sections is None:
            self.sections = []

    def __str__(self):
        results =  (f"\nDepartment: ({self.department_abbreviation})\n"
                f"Course: Course name:{self.course_name}, Course number:{self.course_number}"
                f"\nUnits: {self.units}, Description: {self.description}\n")
        for x in self.sections:
            product = x.section_number
            results = results + '\n' + f'Section numbers: {product}'
        return results

    def add_section(self, section):
        self.sections.append(section)

    def remove_section(self, section):
        self.sections.remove(section)