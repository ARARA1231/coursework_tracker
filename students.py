"""Функции для работы со студентами.

Студенты хранятся в словаре: ключ — id студента,
значение — словарь с данными студента.
"""


def add_student(
    students: dict[int, dict],
    name: str,
    group: str,
    email: str = "",
) -> dict:
    """Добавить студента со следующим свободным id."""
    if not name.strip():
        raise ValueError("ФИО студента не может быть пустым")
    new_id = max(students, default=0) + 1
    student = {
        "id": new_id,
        "name": name.strip(),
        "group": group.strip(),
        "email": email.strip(),
    }
    students[new_id] = student
    return student


def find_student(students: dict[int, dict], student_id: int) -> dict | None:
    """Найти студента по id. Если не найден — вернуть None."""
    return students.get(student_id)


def sort_students(students: dict[int, dict]) -> list[dict]:
    """Вернуть студентов, отсортированных по группе и ФИО."""
    return sorted(
        students.values(),
        key=lambda student: (student["group"], student["name"]),
    )


def show_students(students: dict[int, dict]) -> None:
    """Вывести список студентов."""
    if not students:
        print("Студентов пока нет.")
        return
    for student in sort_students(students):
        print(f"[{student['id']}] {student['name']} ({student['group']})")
