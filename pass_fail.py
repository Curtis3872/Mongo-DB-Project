from mongoengine import *
from enrollment import Enrollment

class PassFail(Enrollment):
    application_date = DateTimeField(required=True)

    def __init__(self, application_date, *args, **values):
        super().__init__(*args, **values)
        self.application_date = application_date

    def __str__(self):
        return f"{Enrollment.__str__(self)},\nSubclass: Pass Fail: Application Date - {self.application_date}"