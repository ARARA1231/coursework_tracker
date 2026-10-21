"""Функции для работы с курсовыми работами.

Курсовые работы хранятся в списке словарей. Связь со студентом
и преподавателем задаётся через student_id и teacher_id.
"""

from datetime import date

STATUS_IN_PROGRESS = "в работе"
STATUS_ON_REVIEW = "на проверке"
STATUS_DEFENDED = "защищена"
STATUSES = (STATUS_IN_PROGRESS, STATUS_ON_REVIEW, STATUS_DEFENDED)


def days_until_deadline(deadline: date, today: date | None = None) -> int:
    """Посчитать, сколько дней осталось до срока сдачи."""
    today = today or date.today()
    return (deadline - today).days


def get_deadline_message(days_left: int) -> str:
    """Сформировать сообщение о сроке сдачи."""
    if days_left < 0:
        return f"Срок сдачи прошёл {abs(days_left)} дн. назад"
    if days_left == 0:
        return "Сегодня последний день сдачи"
    if days_left <= 7:
        return f"Осталось {days_left} дн. — срок близко!"
    return f"До сдачи осталось {days_left} дн."


def get_status_message(status: str) -> str:
    """Вернуть описание статуса курсовой работы."""
    if status == STATUS_IN_PROGRESS:
        return "Студент выполняет работу"
    elif status == STATUS_ON_REVIEW:
        return "Работа передана руководителю на проверку"
    elif status == STATUS_DEFENDED:
        return "Работа защищена"
    return "Неизвестный статус"


def is_active(coursework: dict) -> bool:
    """Активная работа — ещё не защищена."""
    return coursework["status"] != STATUS_DEFENDED


def count_active_for_teacher(courseworks: list[dict], teacher_id: int) -> int:
    """Сколько активных работ у преподавателя."""
    count = 0
    for coursework in courseworks:
        if coursework["teacher_id"] == teacher_id and is_active(coursework):
            count += 1
    return count


def has_active_coursework(courseworks: list[dict], student_id: int) -> bool:
    """Есть ли у студента незащищённая работа."""
    for coursework in courseworks:
        if coursework["student_id"] == student_id and is_active(coursework):
            return True
    return False


def find_coursework(
    courseworks: list[dict], coursework_id: int
) -> dict | None:
    """Найти курсовую работу по id."""
    for coursework in courseworks:
        if coursework["id"] == coursework_id:
            return coursework
    return None


def create_coursework(
    courseworks: list[dict],
    teacher: dict,
    student_id: int,
    title: str,
    deadline: date,
) -> dict:
    """Создать курсовую работу с проверкой правил предметной области."""
    if not title.strip():
        raise ValueError("Тема работы не может быть пустой")
    if has_active_coursework(courseworks, student_id):
        raise ValueError("У студента уже есть активная работа")
    active_count = count_active_for_teacher(courseworks, teacher["id"])
    if active_count >= teacher["max_students"]:
        raise ValueError("У руководителя нет свободных мест")
    new_id = max((cw["id"] for cw in courseworks), default=0) + 1
    coursework = {
        "id": new_id,
        "title": title.strip(),
        "student_id": student_id,
        "teacher_id": teacher["id"],
        "deadline": deadline,
        "status": STATUS_IN_PROGRESS,
        "grade": None,
    }
    courseworks.append(coursework)
    return coursework


def change_status(
    coursework: dict, new_status: str, grade: int | None = None
) -> None:
    """Перевести работу на следующий этап.

    в работе -> на проверке -> защищена (с оценкой),
    на проверке -> в работе (возврат на доработку).
    """
    allowed = {
        STATUS_IN_PROGRESS: (STATUS_ON_REVIEW,),
        STATUS_ON_REVIEW: (STATUS_IN_PROGRESS, STATUS_DEFENDED),
        STATUS_DEFENDED: (),
    }
    if new_status not in allowed[coursework["status"]]:
        raise ValueError(
            f"Нельзя перейти из «{coursework['status']}» в «{new_status}»"
        )
    if new_status == STATUS_DEFENDED:
        if grade is None or not 2 <= grade <= 5:
            raise ValueError("Оценка должна быть от 2 до 5")
        coursework["grade"] = grade
    coursework["status"] = new_status


def filter_by_status(courseworks: list[dict], status: str) -> list[dict]:
    """Отобрать работы с указанным статусом."""
    return [cw for cw in courseworks if cw["status"] == status]


def sort_by_deadline(courseworks: list[dict]) -> list[dict]:
    """Вернуть работы, отсортированные по сроку сдачи."""
    return sorted(courseworks, key=lambda cw: cw["deadline"])
