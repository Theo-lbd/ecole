from models.course import Course
from models.student import Student
from models.teacher import Teacher
from daos.dao import Dao
from typing import Optional


class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO course (name, start_date, end_date, id_teacher) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (course.name, course.start_date, course.end_date, course.teacher.id))
            Dao.connection.commit()
            return cursor.lastrowid

    def read(self, id_course: int) -> Optional[Course]:
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
            if record:
                teacher = self.get_teacher_by_id(record['id_teacher'])
                course = Course(record['name'], record['start_date'], record['end_date'])
                course.id = record['id_course']
                course.teacher = teacher
                course.students_taking_it = self.get_students_by_course_id(course.id)
                return course
            return None

    def update(self, course: Course) -> bool:
        with Dao.connection.cursor() as cursor:
            sql = "UPDATE course SET name=%s, start_date=%s, end_date=%s, id_teacher=%s WHERE id_course=%s"
            cursor.execute(sql, (course.name, course.start_date, course.end_date, course.teacher.id, course.id))
            Dao.connection.commit()
            return cursor.rowcount > 0

    def delete(self, course: Course) -> bool:
        with Dao.connection.cursor() as cursor:
            sql = "DELETE FROM course WHERE id_course=%s"
            cursor.execute(sql, (course.id,))
            Dao.connection.commit()
            return cursor.rowcount > 0

    def get_all_courses(self) -> list[Course]:
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course"
            cursor.execute(sql)
            records = cursor.fetchall()
            courses = []
            for record in records:
                id_teacher = self.get_teacher_by_id(record['id_teacher'])
                course = Course(record['name'], record['start_date'], record['end_date'])
                course.id = record['id_course']
                course.students_taking_it = self.get_students_by_course_id(course.id)
                courses.append(course)
            return courses

    def get_teacher_by_id(self, id_teacher: int) -> Optional[Teacher]:
        ...
        return None

    def get_students_by_course_id(self, id_course: int) -> list[Student]:
        ...
        return []
