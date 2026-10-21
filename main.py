"""Консольное приложение «Учёт курсовых работ»."""

from courseworks import (
    STATUS_DEFENDED,
    STATUS_IN_PROGRESS,
    STATUS_ON_REVIEW,
    STATUSES,
    change_status,
    count_active_for_teacher,
    create_coursework,
    days_until_deadline,
    filter_by_status,
    find_coursework,
    get_deadline_message,
    get_status_message,
    sort_by_deadline,
)
from storage import (
    load_courseworks,
    load_students,
    load_teachers,
    save_courseworks,
    save_students,
)
from students import add_student, find_student, show_students
from teachers import can_take_student, find_teacher, sort_teachers
from utils import input_date, input_int, input_text

MENU = """
===== Учёт курсовых работ =====
1. Список студентов
2. Список преподавателей
3. Список курсовых работ
4. Курсовые работы по статусу
5. Подробно о курсовой работе
6. Создать курсовую работу
7. Сдать работу на проверку
8. Вернуть работу на доработку
9. Отметить защиту и выставить оценку
10. Добавить студента
0. Выход
"""


def show_teachers(teachers: dict[int, dict], courseworks: list[dict]) -> None:
    """Вывести преподавателей с текущей занятостью."""
    for teacher in sort_teachers(teachers):
        active = count_active_for_teacher(courseworks, teacher["id"])
        free = "есть места" if can_take_student(
            active, teacher["max_students"]
        ) else "мест нет"
        print(
            f"[{teacher['id']}] {teacher['name']} — занято {active} "
            f"из {teacher['max_students']} ({free})"
        )


def show_courseworks(
    courseworks: list[dict], students: dict[int, dict]
) -> None:
    """Вывести курсовые работы, отсортированные по сроку сдачи."""
    if not courseworks:
        print("Курсовых работ нет.")
        return
    for coursework in sort_by_deadline(courseworks):
        student = students[coursework["student_id"]]
        print(
            f"[{coursework['id']}] «{coursework['title']}» — "
            f"{student['name']} [{coursework['status']}], срок "
            f"{coursework['deadline'].strftime('%d.%m.%Y')}"
        )


def show_coursework_details(
    coursework: dict, students: dict[int, dict], teachers: dict[int, dict]
) -> None:
    """Вывести подробную информацию о курсовой работе."""
    student = students[coursework["student_id"]]
    teacher = teachers[coursework["teacher_id"]]
    print(f"Тема: {coursework['title']}")
    print(f"Студент: {student['name']}, группа {student['group']}")
    print(f"Руководитель: {teacher['name']}")
    print(f"Срок сдачи: {coursework['deadline'].strftime('%d.%m.%Y')}")
    if coursework["status"] != STATUS_DEFENDED:
        days_left = days_until_deadline(coursework["deadline"])
        print(get_deadline_message(days_left))
    print(f"Статус: {get_status_message(coursework['status'])}")
    print(f"Оценка: {coursework['grade'] or 'не выставлена'}")


def ask_status() -> str:
    """Предложить выбрать статус из списка."""
    for number, status in enumerate(STATUSES, start=1):
        print(f"{number}. {status}")
    choice = input_int("Выберите статус: ", 1, len(STATUSES))
    return STATUSES[choice - 1]


def scenario_create(
    students: dict[int, dict],
    teachers: dict[int, dict],
    courseworks: list[dict],
) -> None:
    """Создать курсовую работу."""
    show_students(students)
    student_id = input_int("id студента: ", 1)
    if find_student(students, student_id) is None:
        print("Студент не найден.")
        return
    show_teachers(teachers, courseworks)
    teacher = find_teacher(teachers, input_int("id руководителя: ", 1))
    if teacher is None:
        print("Преподаватель не найден.")
        return
    title = input_text("Тема работы: ")
    deadline = input_date("Срок сдачи (ДД.ММ.ГГГГ): ")
    try:
        coursework = create_coursework(
            courseworks, teacher, student_id, title, deadline
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    save_courseworks(courseworks)
    print(f"Создана работа №{coursework['id']}")


def scenario_change_status(courseworks: list[dict], new_status: str) -> None:
    """Перевести работу на другой этап."""
    coursework = find_coursework(
        courseworks, input_int("Введите id курсовой работы: ", 1)
    )
    if coursework is None:
        print("Курсовая работа не найдена.")
        return
    grade = None
    if new_status == STATUS_DEFENDED:
        if coursework["status"] != STATUS_ON_REVIEW:
            print("Ошибка: защитить можно только работу на проверке")
            return
        grade = input_int("Оценка (2–5): ", 2, 5)
    try:
        change_status(coursework, new_status, grade)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    save_courseworks(courseworks)
    print(f"Новый статус: {coursework['status']}")


def scenario_add_student(students: dict[int, dict]) -> None:
    """Добавить студента."""
    name = input_text("ФИО студента: ")
    group = input_text("Группа: ")
    email = input("Email (можно пропустить): ")
    student = add_student(students, name, group, email)
    save_students(students)
    print(f"Добавлен студент №{student['id']}")


def main() -> None:
    """Точка входа: загрузка данных и главное меню."""
    try:
        students = load_students()
        teachers = load_teachers()
        courseworks = load_courseworks()
    except ValueError as error:
        print(f"Не удалось загрузить данные: {error}")
        return

    while True:
        print(MENU)
        choice = input_int("Выберите пункт: ", 0, 10)
        print()
        if choice == 0:
            print("До свидания!")
            break
        elif choice == 1:
            show_students(students)
        elif choice == 2:
            show_teachers(teachers, courseworks)
        elif choice == 3:
            show_courseworks(courseworks, students)
        elif choice == 4:
            selected = filter_by_status(courseworks, ask_status())
            show_courseworks(selected, students)
        elif choice == 5:
            coursework = find_coursework(
                courseworks, input_int("Введите id курсовой работы: ", 1)
            )
            if coursework is None:
                print("Курсовая работа не найдена.")
            else:
                show_coursework_details(coursework, students, teachers)
        elif choice == 6:
            scenario_create(students, teachers, courseworks)
        elif choice == 7:
            scenario_change_status(courseworks, STATUS_ON_REVIEW)
        elif choice == 8:
            scenario_change_status(courseworks, STATUS_IN_PROGRESS)
        elif choice == 9:
            scenario_change_status(courseworks, STATUS_DEFENDED)
        elif choice == 10:
            scenario_add_student(students)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nРабота программы прервана.")
