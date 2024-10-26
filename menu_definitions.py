from Menu import Menu
import logging
from Option import Option

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add()"),
    Option("Delete existing instance", "delete()"),
    Option("List existing instances", "list_members()"),
    Option("Drop Database", "drop_collection()"),
    Option("Exit", "exit()")
])

add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Departments", "add_department()"),
    Option("Courses", "add_course()"),
    Option("Sections", "add_section()"),
    Option("Students", "add_student()"),
    Option("Major", "add_major()"),
    Option("Student Majors", "add_student_major()"),
    Option("Enrollments", "add_enrollment()"),
    Option("Exit", "pass")
])

delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Departments", "delete_department()"),
    Option("Courses", "delete_course()"),
    Option("Sections", "delete_section()"),
    Option("Students", "delete_student()"),
    Option("Major", "delete_major()"),
    Option("Student Majors", "delete_student_major()"),
    Option("Enrollments", "delete_enrollment()"),
    Option("Exit", "pass")
])

list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Departments", "list_departments()"),
    Option("Courses", "list_courses()"),
    Option("Sections", "list_sections()"),
    Option("Students", "list_students()"),
    Option("Major", "list_majors()"),
    Option("Enrollments", "list_enrollments()"),
    Option("Exit", "pass")
])