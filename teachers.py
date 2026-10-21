"""Функции для работы с преподавателями.

Преподаватели хранятся в словаре: ключ — id преподавателя,
значение — словарь с данными преподавателя.
"""


def can_take_student(current_students: int, max_students: int) -> bool:
    """Проверить, может ли преподаватель взять ещё одного студента."""
    return current_students < max_students


def add_teacher(
    teachers: dict[int, dict],
    name: str,
    department: str,
    email: str = "",
    max_students: int = 5,
) -> dict:
    """Добавить преподавателя со следующим свободным id."""
    if not name.strip():
        raise ValueError("ФИО преподавателя не может быть пустым")
    if max_students < 1:
        raise ValueError("Лимит студентов должен быть больше нуля")
    new_id = max(teachers, default=0) + 1
    teacher = {
        "id": new_id,
        "name": name.strip(),
        "department": department.strip(),
        "email": email.strip(),
        "max_students": max_students,
    }
    teachers[new_id] = teacher
    return teacher


def find_teacher(teachers: dict[int, dict], teacher_id: int) -> dict | None:
    """Найти преподавателя по id. Если не найден — вернуть None."""
    return teachers.get(teacher_id)


def sort_teachers(teachers: dict[int, dict]) -> list[dict]:
    """Вернуть преподавателей, отсортированных по ФИО."""
    return sorted(teachers.values(), key=lambda teacher: teacher["name"])
