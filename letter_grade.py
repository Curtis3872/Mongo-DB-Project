from mongoengine import *
from enrollment import Enrollment

class LetterGrade(Enrollment):
    min_satisfactory = StringField(choices=['A', 'B', 'C'], required=True)

    def __init__(self, min_satisfactory, *args, **values):
        if min_satisfactory not in ['A', 'B', 'C']:
            raise ValueError("Invalid grade choice")
        super().__init__(*args, **values)
        self.min_satisfactory = min_satisfactory

    def __str__(self):
        return f"{Enrollment.__str__(self)}, Letter Grade: Min Satisfactory - {self.min_satisfactory}"
