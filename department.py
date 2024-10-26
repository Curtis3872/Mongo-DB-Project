from mongoengine import *

class Department(Document):
    name = StringField(max_length=50, required=True)
    abbreviation = StringField(max_length=6, required=True)
    chair_name = StringField(max_length=80, required=True)
    building = StringField(choices=['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                           required=True)
    office = IntField(required=True)
    description = StringField(max_length=80, required=True)
    courses = ListField(ReferenceField('Course'))
    majors = ListField(ReferenceField('Major'))

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'departments_uk_1'},
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_uk_2'}]}
    def __init__(self, name:str, abbreviation:str, chair_name:str, building:str, office:int, description:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.abbreviation = abbreviation
        self.chair_name = chair_name
        self.building = building
        self.office = office
        self.description = description
        if self.courses is None:
            self.courses = []
        if self.majors is None:
            self.majors = []

    def __str__(self):
        results = (f"Department: {self.name} ({self.abbreviation})\nChair: {self.chair_name}"
                   f"\nLocation: {self.building}, {self.office}\nDescription: {self.description}")
        for x in self.courses:
            product = x.course_name
            results = results + '\n' + f'Courses: {product}'
        for y in self.majors:
            product = y.name
            results = results + '\n' + f'Majors: {product}'
        return  results

    def add_course(self, course):
        self.courses.append(course)

    def remove_course(self, course):
        self.courses.remove(course)

    def add_major(self, major):
        self.majors.append(major)

    def remove_major(self, major):
        self.majors.remove(major)

