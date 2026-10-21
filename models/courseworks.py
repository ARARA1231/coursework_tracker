"""Курсовые работы: класс Coursework и функции работы с коллекцией."""

from datetime import date

from models.students import Student
from models.teachers import Teacher

STATUS_IN_PROGRESS = "в работе"
STATUS_ON_REVIEW = "на проверке"
STATUS_DEFENDED = "защищена"
STATUSES = (STATUS_IN_PROGRESS, STATUS_ON_REVIEW, STATUS_DEFENDED)

MIN_GRADE = 2
MAX_GRADE = 5


def get_deadline_message(days_left: int) -> str:
    """Сформировать сообщение о сроке сдачи (функция из ПР1)."""
    if days_left < 0:
        return f"Срок сдачи прошёл {abs(days_left)} дн. назад"
    if days_left == 0:
        return "Сегодня последний день сдачи"
    if days_left <= 7:
        return f"Осталось {days_left} дн. — срок близко!"
    return f"До сдачи осталось {days_left} дн."


def get_status_message(status: str) -> str:
    """Вернуть описание статуса курсовой работы (функция из ПР1)."""
    if status == STATUS_IN_PROGRESS:
        return "Студент выполняет работу"
    elif status == STATUS_ON_REVIEW:
        return "Работа передана руководителю на проверку"
    elif status == STATUS_DEFENDED:
        return "Работа защищена"
    return "Неизвестный статус"


class Coursework:
    """Курсовая работа: связывает студента и преподавателя."""

    def __init__(
        self,
        coursework_id: int,
        title: str,
        student: Student,
        teacher: Teacher,
        deadline: date,
        status: str = STATUS_IN_PROGRESS,
        grade: int | None = None,
    ) -> None:
        if status not in STATUSES:
            raise ValueError(f"Неизвестный статус: {status}")
        self.id = coursework_id
        self.title = title
        self.student = student
        self.teacher = teacher
        self.deadline = deadline
        self.status = status
        self.grade = grade

    @property
    def is_active(self) -> bool:
        """Активная работа — ещё не защищена."""
        return self.status != STATUS_DEFENDED

    def days_left(self, today: date | None = None) -> int:
        """Сколько дней осталось до срока сдачи."""
        today = today or date.today()
        return (self.deadline - today).days

    @property
    def is_overdue(self) -> bool:
        """Срок прошёл, а работа всё ещё выполняется."""
        return self.status == STATUS_IN_PROGRESS and self.days_left() < 0

    @property
    def deadline_message(self) -> str:
        """Сообщение о сроке: для защищённой работы срок уже не важен."""
        if not self.is_active:
            return "Работа защищена, срок соблюдён"
        return get_deadline_message(self.days_left())

    @property
    def status_message(self) -> str:
        """Описание текущего статуса."""
        return get_status_message(self.status)

    def submit(self) -> None:
        """Сдать работу на проверку руководителю."""
        if self.status != STATUS_IN_PROGRESS:
            raise ValueError("Сдать на проверку можно только работу в работе")
        self.status = STATUS_ON_REVIEW

    def return_to_work(self) -> None:
        """Вернуть работу студенту на доработку."""
        if self.status != STATUS_ON_REVIEW:
            raise ValueError("Вернуть можно только работу на проверке")
        self.status = STATUS_IN_PROGRESS

    def defend(self, grade: int) -> None:
        """Отметить защиту и выставить оценку."""
        if self.status != STATUS_ON_REVIEW:
            raise ValueError("Защитить можно только работу на проверке")
        if not MIN_GRADE <= grade <= MAX_GRADE:
            raise ValueError(
                f"Оценка должна быть от {MIN_GRADE} до {MAX_GRADE}"
            )
        self.grade = grade
        self.status = STATUS_DEFENDED

    def __str__(self) -> str:
        return f"«{self.title}» — {self.student.name} [{self.status}]"


def find_coursework(
    courseworks: list[Coursework], coursework_id: int
) -> Coursework | None:
    """Найти курсовую работу по id. Если не найдена — вернуть None."""
    for coursework in courseworks:
        if coursework.id == coursework_id:
            return coursework
    return None


def get_student_courseworks(
    courseworks: list[Coursework], student: Student
) -> list[Coursework]:
    """Все работы студента."""
    return [cw for cw in courseworks if cw.student.id == student.id]


def get_teacher_courseworks(
    courseworks: list[Coursework], teacher: Teacher
) -> list[Coursework]:
    """Все работы, которыми руководит преподаватель."""
    return [cw for cw in courseworks if cw.teacher.id == teacher.id]


def count_active_for_teacher(
    courseworks: list[Coursework], teacher: Teacher
) -> int:
    """Сколько активных (не защищённых) работ у преподавателя."""
    return sum(
        1 for cw in get_teacher_courseworks(courseworks, teacher)
        if cw.is_active
    )


def has_active_coursework(
    courseworks: list[Coursework], student: Student
) -> bool:
    """Есть ли у студента незащищённая курсовая работа."""
    return any(
        cw.is_active for cw in get_student_courseworks(courseworks, student)
    )


def create_coursework(
    courseworks: list[Coursework],
    title: str,
    student: Student,
    teacher: Teacher,
    deadline: date,
) -> Coursework:
    """Создать курсовую работу с проверкой правил предметной области."""
    if not title.strip():
        raise ValueError("Тема работы не может быть пустой")
    if has_active_coursework(courseworks, student):
        raise ValueError(f"У студента {student.name} уже есть активная работа")
    active_count = count_active_for_teacher(courseworks, teacher)
    if not teacher.has_free_slots(active_count):
        raise ValueError(f"У руководителя {teacher.name} нет свободных мест")
    new_id = max((cw.id for cw in courseworks), default=0) + 1
    coursework = Coursework(new_id, title.strip(), student, teacher, deadline)
    courseworks.append(coursework)
    return coursework


def filter_by_status(
    courseworks: list[Coursework], status: str
) -> list[Coursework]:
    """Отобрать работы с указанным статусом."""
    return [cw for cw in courseworks if cw.status == status]


def sort_by_deadline(courseworks: list[Coursework]) -> list[Coursework]:
    """Вернуть работы, отсортированные по сроку сдачи."""
    return sorted(courseworks, key=lambda cw: cw.deadline)
