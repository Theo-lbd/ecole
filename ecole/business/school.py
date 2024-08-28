# school.py
from dataclasses import dataclass, field
from daos.course_dao import CourseDao
from models.course import Course
from models.teacher import Teacher
from models.student import Student

@dataclass
class School:
    courses: list[Course] = field(default_factory=list, init=False)
    teachers: list[Teacher] = field(default_factory=list, init=False)
    students: list[Student] = field(default_factory=list, init=False)

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    def add_teacher(self, teacher: Teacher) -> None:
        self.teachers.append(teacher)

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def display_courses_list(self) -> None:
        if not self.courses:
            print("Aucun cours disponible.")
        else:
            for course in self.courses:
                print(course)
                for student in course.students_taking_it:
                    print(f"- {student.name}")
                print()

    @staticmethod
    def get_course_by_id(id_course: int):
        course_dao: CourseDao = CourseDao()
        return course_dao.read(id_course)

    def load_courses_from_db(self) -> None:
        course_dao = CourseDao()
        self.courses = course_dao.get_all_courses()
