"""
    We can define classes called person and courses
    
    Person (att: name, id, age | met: quit)
        students (att: major, GPA, courses, professors | met: enroll)
        faculty (att: department, rank, students, courses | met: apply)
        parttimers (att: major, gpa, courses, department, rank, students, professors | met: enroll, apply)

    Courses (att: name, code, instructor(obj), students)

    Print their info:
    All students (name, ID, major, GPA).
All faculty (name, ID, department, rank).
All courses (course name, course code, instructor, and list of enrolled students).
All courses a specific student is enrolled in.
All students taught by a specific faculty member.
Add new students, faculty, and courses: The system should allow the university administrator to add new students, faculty, and courses.

"""

class Person:
    def __init__(self, name, age, id, courses):
        self.name = name
        self.age = age
        self.id = id
        self.courses =  courses
    
    def quit(self):
        # good addition here
        pass

class Student(Person):
    def __init__(self, name, age, id, courses, major, GPA):
        super().__init__(name, age, id)
        self.major = major
        self.GPA = GPA

    def enorll(self, courses):
        self.courses.append(courses)

class Faculty(Person):
    def __init__(self, name, age, id, courses, department, rank):
        super().__init__(name, age, id)
        self.department = department
        self.rank = rank

    def apply(self, courses):
        self.courses.append(courses)
    
class Parttimer(Student, Faculty):
    def __init__(self, name, age, id, courses, major, GPA, department, rank):
        super().__init__() # we need to rethink this







