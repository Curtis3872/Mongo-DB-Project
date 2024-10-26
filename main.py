from ConstraintUtilities import select_general, unique_general
from Utilities import Utilities
from Menu import Menu
from Option import Option
from menu_definitions import menu_main, add_select, list_select, delete_select
from department import Department
from course import Course
from section import Section
from student import Student
from enrollment import Enrollment
from student_major import StudentMajor
from major import Major
from pass_fail import PassFail
from letter_grade import LetterGrade
import datetime
import time

def menu_loop(menu: Menu):
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)

def add():
    menu_loop(add_select)

def list_members():
    menu_loop(list_select)

def delete():
    menu_loop(delete_select)

def drop_collection():
    db.drop_database('cecs-323-spring-2024-cl')
    print("Database deleted.")

def prompt_for_enum(prompt: str, cls, attribute_name: str):
    attr = getattr(cls, attribute_name)
    if type(attr).__name__ == 'EnumField':
        enum_values = []
        for choice in attr.choices:
            enum_values.append(Option(choice.value, choice))
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')

def add_department():
    success: bool = False
    while not success:
        new_department = Department(input("Department Name --> "),
                                    input("Abbreviation --> "),
                                    input("Chair Name --> "),
                                    input("Building --> "),
                                    int(input("Office Number --> ")),
                                    input("Description --> "))
        violated_constraints = unique_general(new_department)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        try:
            new_department.save()
            print("Department added")
            success = True
        except Exception as e:
            print(e)
            print('Errors storing the new department:')
            Utilities.print_exception(e)

def add_course():
    success: bool = False
    while not success:
        new_department = select_department()
        abbrev = new_department.abbreviation
        new_course = Course(
            new_department,
            abbrev,
            input("Course Name --> "),
            input("Course Number --> "),
            int(input("Units --> ")),
            input("Description --> ")
        )
        violated_constraints = unique_general(new_course)
        if len(violated_constraints):
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
                print('try again')
        else:
            try:
                new_course.save()
                Department.add_course(new_department,new_course)
                new_department.save()
                print("Course added")
                success = True
            except Exception as e:
                print(e)
                print('Errors storing the new course:')
                print(Utilities.print_exception(e))

def add_section():
    success: bool = False
    while not success:
        new_course = select_course()
        course_name = new_course.course_name
        course_number = new_course.course_number
        abbrev = new_course.department_abbreviation
        print("Make the section")
        section_number = int(input("Section number --> "))
        semester = input("Semester --> ")
        section_year = int(input("Section year --> "))
        building = input("Building --> ")
        room = int(input("Room --> "))
        schedule = input("Schedule --> ")
        class_time = input("Class time HH:MM--> ")
        new_time = time.strptime(class_time, "%H:%M")
        if new_time < time.strptime('8:00',"%H:%M") or new_time > time.strptime('19:30',"%H:%M"):
            print("Error time must between 8:00 and 19:30")
            break
        instructor = input("Instructor --> ")
        new_section = Section(
            abbrev, course_name, course_number, section_number, semester, section_year,
            building, room, schedule, class_time, instructor)
        violated_constraints = unique_general(new_section)
        if len(violated_constraints):
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
                print('try again')
        else:
            try:
                new_section.save()
                Course.add_section(new_course, new_section)
                new_course.save()
                print("Section added")
                success = True
            except Exception as e:
                print(e)
                print('Errors storing the new section:')
                print(Utilities.print_exception(e))

def add_major():
    success: bool = False
    while not success:
        new_department = select_department()
        new_major = Major(
            new_department.id,
            input("Major Name --> "),
            input("Description --> "),
        )
        violated_constraints = unique_general(new_major)
        if len(violated_constraints):
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
                print('try again')
        else:
            try:
                new_major.save()
                Department.add_major(new_department,new_major)
                new_department.save()
                print("Major added")
                success = True
            except Exception as e:
                print(e)
                print('Errors storing the new major:')
                print(Utilities.print_exception(e))

def add_student():
    success: bool = False
    while not success:
        new_student = Student(
            input("Last Name --> "),
            input("First name --> "),
            input("Email --> ")
        )
        violated_constraints = unique_general(new_student)
        if len(violated_constraints):
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
                print('try again')
        else:
            try:
                new_student.save()
                print("Student added")
                success = True
            except Exception as e:
                print(e)
                print('Errors storing the new student:')
                print(Utilities.print_exception(e))

def add_student_major():
    print("Adding student to a Major")
    success: bool = False
    today = datetime.date.today()
    while not success:
        students = select_student()
        majors = select_major()
        major_name = majors.name
        date = input("Declaration Date mm/dd/yyyy--> ")
        declaration_date = datetime.datetime.strptime(date, "%m/%d/%Y").date()
        studentid = students.id
        if declaration_date > today:
            print("The date entered is in the future. Please enter a valid date.")
            print("Student Major not added")
            break
        newstudentmajors = StudentMajor(major_name=major_name,declaration_date=declaration_date,student_id=studentid)
        try:
            Student.add_majors(students,newstudentmajors)
            Major.add_student(majors,newstudentmajors)
            students.save()
            majors.save()
            print("Student major added")
            success = True
        except Exception as e:
            print(e)
            print('Errors storing the new student:')
            print(Utilities.print_exception(e))

def add_enrollment():
    print("Enrolling student into a Section")
    success: bool = False
    choice = 0
    while not success:
        selected_students = select_student()
        selected_section = select_section()
        abbrev = selected_section.department_abbreviation
        id = selected_students.id
        course_name = selected_section.course_name
        course_number = selected_section.course_number
        sec_num = selected_section.section_number
        semester = selected_section.semester
        section_year = selected_section.section_year
        while choice != 1 or choice != 2:
            choice = int(input("Choose Subclass: 1.Letter grade, 2. Pass Fail-->"))
            if choice == 1:
                new_enrollment = LetterGrade(student_id=id, department_abbreviation=abbrev, course_name=course_name,
                                             course_number=course_number, section_number=sec_num, semester=semester,
                                             section_year=section_year,
                                             min_satisfactory=input("Minimum Satisfactory Grade:"))
                try:
                    Enrollment.objects.get(
                        student_id=id, department_abbreviation=abbrev, course_name=course_name,
                        course_number=course_number, section_number=sec_num, semester=semester,
                        section_year=section_year)
                    print("There is already an enrollment of these attributes")
                    break
                except:
                    try:
                        new_enrollment.save()
                        Student.add_enrollment(selected_students, new_enrollment)
                        Section.add_enrollment(selected_section, new_enrollment)
                        selected_students.save()
                        selected_section.save()
                        print("Enrollment added")
                        success = True
                        break
                    except Exception as e:
                        print(e)
                        print('Errors enrolling student:')
                        print(Utilities.print_exception(e))
            elif choice == 2:
                today = datetime.date.today()
                try:
                    user_date = input("Application Date: mm/dd/yyyy-->")
                    app_date = datetime.datetime.strptime(user_date, "%m/%d/%Y").date()
                    if app_date > today:
                        raise ValueError("The date entered is in the future. Please enter a valid date.")
                    new_enrollment = PassFail(student_id=id, department_abbreviation=abbrev, course_name=course_name,
                                              course_number=course_number, section_number=sec_num, semester=semester,
                                              section_year=section_year,
                                              application_date=app_date)
                except Exception as e:
                    print(e)
                    break
                try:
                    Enrollment.objects.get(
                        student_id=id, department_abbreviation=abbrev, course_name=course_name,
                        course_number=course_number, section_number=sec_num, semester=semester,
                        section_year=section_year)
                    print("There is already an enrollment of these attributes")
                    break
                except:
                    try:
                        new_enrollment.save()
                        Student.add_enrollment(selected_students, new_enrollment)
                        Section.add_enrollment(selected_section, new_enrollment)
                        selected_students.save()
                        selected_section.save()
                        print("Enrollment added")
                        success = True
                        break
                    except Exception as e:
                        print(e)
                        print('Errors enrolling student:')
                        print(Utilities.print_exception(e))

def select_department():
    print("Selecting Department")
    return select_general(Department)

def select_course():
    print("Selecting Course")
    return select_general(Course)

def select_section():
    print("Selecting Section")
    return select_general(Section)

def select_student():
    print("Selecting Student")
    return select_general(Student)

def select_enrollment():
    print("Selecting Enrollment")
    return select_general(Enrollment)
def select_major():
    print("Selecting Major")
    return select_general(Major)

def delete_department():
    department = select_department()
    courses_count = len(department.courses)
    major_count = len(department.majors)
    if courses_count > 0 or major_count > 0:
        print(f"{department.name} has one or more courses or majors in it.")
        print("Cannot delete. Try again.")
        return
    department.delete()
    print(f"Department has been deleted.")

def delete_course():
    selected_course = select_course()
    sections_count = len(selected_course.sections)
    if sections_count > 0:
        print(f"The course {selected_course.course_name} has one or more sections in it.")
        print("Cannot delete. Try again.")
        return
    department = Department.objects(abbreviation=selected_course.department_abbreviation).first()
    Department.remove_course(department,selected_course)
    department.save()
    selected_course.delete()
    print(f"Course has been deleted.")

def delete_section():
    selected_section = select_section()
    enrollments_count = len(selected_section.enrollments)
    if enrollments_count > 0:
        print(f"Section {selected_section.section_number} has one or more enrollments. Cannot delete.")
        return
    course = Course.objects(department_abbreviation=selected_section.department_abbreviation,
                            course_name=selected_section.course_name).first()
    Course.remove_section(course,selected_section)
    course.save()
    selected_section.delete()
    print(f"Section has been deleted.")


def delete_student():
    selected_student = select_student()
    enrollments_count = len(selected_student.enrollments)
    if enrollments_count > 0:
        print(f"Student :{selected_student.lastname},{selected_student.firstname} has one or more enrollments. Cannot delete.")
        return
    selected_student.delete()
    print(f"Student has been deleted.")

def delete_major():
    selected_major = select_major()
    student_count = len(selected_major.students)
    if student_count > 0:
        print(f"Major: {selected_major.name} has one or more sections. Cannot deleted.")
        print("Try again.")
    department = Department.objects(id=selected_major.department).first()
    Department.remove_major(department,selected_major)
    department.save()
    selected_major.delete()
    print(f"Major has been deleted.")

def delete_student_major():
    selected_student = select_student()
    selected_major = select_major()
    student_major = next((sm for sm in selected_student.majors if sm.major_name == selected_major.name), None)
    if student_major:
        selected_student.majors.remove(student_major)
        selected_student.save()
        print("Removed major from student.")

    major_student = next((ms for ms in selected_major.students if ms.student_id == selected_student.id), None)
    if major_student:
        selected_major.students.remove(major_student)
        selected_major.save()
        print("Removed student from major.")

def delete_enrollment():
    selected_enrollment = select_enrollment()
    studentid = selected_enrollment.student_id
    student = Student.objects(id=studentid).first()
    course_name = selected_enrollment.course_name
    section_number = selected_enrollment.section_number
    section_year = selected_enrollment.section_year
    semester = selected_enrollment.semester
    Student.remove_enrollment(student, selected_enrollment)
    student.save()
    print("Student removed section")

    section = Section.objects(course_name=course_name,section_number=section_number,section_year=section_year,semester=semester).first()
    Section.remove_enrollment(section,selected_enrollment)
    section.save()
    print("Section removed student")

    selected_enrollment.delete()
    print("Enrollment deleted")

def list_departments():
    for department in Department.objects:
        print(department)

def list_courses():
    selected_department = select_department()
    for course in selected_department.courses:
        print(course)

def list_sections():
    selected_department = select_department()
    selected_course = select_course()
    for section in Section.objects(department_abbreviation=selected_department.abbreviation,
                                   course_name=selected_course.course_name):
        print(section)

def list_students():
    for x in Student.objects:
        print(x)
    return

def list_enrollments():
    for x in Enrollment.objects:
        print(x)
    return

def list_majors():
    for x in Major.objects:
        print(x)
    return

if __name__ == '__main__':
    print('Starting in main.')
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

