"""Преподаватели: класс Teacher и функции работы с коллекцией."""


class Teacher:
    """Преподаватель — руководитель курсовых работ."""

    def __init__(
        self,
        teacher_id: int,
        name: str,
        department: str,
        email: str = "",
        max_students: int = 5,
    ) -> None:
        if max_students < 1:
            raise ValueError("Лимит студентов должен быть больше нуля")
        self.id = teacher_id
        self.name = name
        self.department = department
        self.email = email
        self.max_students = max_students

    def has_free_slots(self, active_count: int) -> bool:
        """Может ли преподаватель взять ещё одного студента."""
        return active_count < self.max_students

    def free_slots(self, active_count: int) -> int:
        """Сколько свободных мест осталось у руководителя."""
        return max(self.max_students - active_count, 0)

    def __str__(self) -> str:
        return f"{self.name}, {self.department}"


def add_teacher(
    teachers: list[Teacher],
    name: str,
    department: str,
    email: str = "",
    max_students: int = 5,
) -> Teacher:
    """Создать преподавателя со следующим свободным id и добавить в список."""
    if not name.strip():
        raise ValueError("ФИО преподавателя не может быть пустым")
    new_id = max((teacher.id for teacher in teachers), default=0) + 1
    teacher = Teacher(
        new_id, name.strip(), department.strip(), email.strip(), max_students
    )
    teachers.append(teacher)
    return teacher


def find_teacher(teachers: list[Teacher], teacher_id: int) -> Teacher | None:
    """Найти преподавателя по id. Если не найден — вернуть None."""
    for teacher in teachers:
        if teacher.id == teacher_id:
            return teacher
    return None


def sort_teachers(teachers: list[Teacher]) -> list[Teacher]:
    """Вернуть преподавателей, отсортированных по ФИО."""
    return sorted(teachers, key=lambda teacher: teacher.name)
