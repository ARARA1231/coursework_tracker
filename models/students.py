"""Студенты: класс Student и функции работы с коллекцией студентов."""


class Student:
    """Студент, выполняющий курсовую работу."""

    def __init__(
        self,
        student_id: int,
        name: str,
        group: str,
        email: str = "",
    ) -> None:
        self.id = student_id
        self.name = name
        self.group = group
        self.email = email

    def __str__(self) -> str:
        return f"{self.name} ({self.group})"


def add_student(
    students: list[Student],
    name: str,
    group: str,
    email: str = "",
) -> Student:
    """Создать студента со следующим свободным id и добавить в список."""
    if not name.strip():
        raise ValueError("ФИО студента не может быть пустым")
    new_id = max((student.id for student in students), default=0) + 1
    student = Student(new_id, name.strip(), group.strip(), email.strip())
    students.append(student)
    return student


def find_student(students: list[Student], student_id: int) -> Student | None:
    """Найти студента по id. Если не найден — вернуть None."""
    for student in students:
        if student.id == student_id:
            return student
    return None


def sort_students(students: list[Student]) -> list[Student]:
    """Вернуть студентов, отсортированных по группе и ФИО."""
    return sorted(students, key=lambda student: (student.group, student.name))
