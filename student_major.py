from mongoengine import *

class StudentMajor(EmbeddedDocument):
    major_name = StringField(max_length=100, required=True)
    declaration_date = DateTimeField(required=True)
    student_id = ObjectIdField(max_length=100, required=True)

    meta = {'collection': 'student_majors',
            'indexes': [
                {'unique': True, 'fields': ['student_id', 'major_name'], 'name': 'student_majors_uk_1'}
            ]}

    def __init__(self, major_name, declaration_date, student_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.major_name = major_name
        self.declaration_date = declaration_date
        self.student_id = student_id

    def __str__(self):
        return f"Major: {self.name}\ndeclaration date: {self.declaration_date}"