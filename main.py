"""Консольное приложение «Учёт курсовых работ» (ПР1–ПР3)."""

from models.courseworks import (
    STATUS_ON_REVIEW,
    STATUSES,
    Coursework,
    count_active_for_teacher,
    create_coursework,
    filter_by_status,
    find_coursework,
    sort_by_deadline,
)
from models.students import Student, add_student, find_student, sort_students
from models.teachers import Teacher, add_teacher, find_teacher, sort_teachers
from storage import load_all, save_courseworks, save_students, save_teachers
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
11. Добавить преподавателя
0. Выход
"""


def show_students(students: list[Student]) -> None:
    """Вывести список студентов."""
    if not students:
        print("Студентов пока нет.")
        return
    for student in sort_students(students):
        print(f"[{student.id}] {student}")


def show_teachers(
    teachers: list[Teacher], courseworks: list[Coursework]
) -> None:
    """Вывести преподавателей с текущей занятостью."""
    if not teachers:
        print("Преподавателей пока нет.")
        return
    for teacher in sort_teachers(teachers):
        active = count_active_for_teacher(courseworks, teacher)
        print(
            f"[{teacher.id}] {teacher} — занято {active} "
            f"из {teacher.max_students}"
        )


def show_courseworks(courseworks: list[Coursework]) -> None:
    """Вывести курсовые работы, отсортированные по сроку сдачи."""
    if not courseworks:
        print("Курсовых работ нет.")
        return
    for coursework in sort_by_deadline(courseworks):
        print(
            f"[{coursework.id}] {coursework} — срок "
            f"{coursework.deadline.strftime('%d.%m.%Y')}"
        )


def show_coursework_details(coursework: Coursework) -> None:
    """Вывести подробную информацию о курсовой работе."""
    grade = coursework.grade if coursework.grade else "не выставлена"
    print(f"Тема: {coursework.title}")
    print(f"Студент: {coursework.student}")
    print(f"Руководитель: {coursework.teacher}")
    print(f"Срок сдачи: {coursework.deadline.strftime('%d.%m.%Y')}")
    print(coursework.deadline_message)
    print(f"Статус: {coursework.status} — {coursework.status_message}")
    print(f"Оценка: {grade}")


def ask_coursework(courseworks: list[Coursework]) -> Coursework | None:
    """Спросить id работы и найти её."""
    coursework_id = input_int("Введите id курсовой работы: ", min_value=1)
    coursework = find_coursework(courseworks, coursework_id)
    if coursework is None:
        print("Курсовая работа не найдена.")
    return coursework


def ask_status() -> str:
    """Предложить выбрать статус из списка."""
    for number, status in enumerate(STATUSES, start=1):
        print(f"{number}. {status}")
    choice = input_int("Выберите статус: ", 1, len(STATUSES))
    return STATUSES[choice - 1]


def scenario_create_coursework(
    students: list[Student],
    teachers: list[Teacher],
    courseworks: list[Coursework],
) -> None:
    """Создать курсовую работу: выбрать студента, руководителя, тему, срок."""
    show_students(students)
    student = find_student(students, input_int("id студента: ", 1))
    if student is None:
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
            courseworks, title, student, teacher, deadline
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    save_courseworks(courseworks)
    print(f"Создана работа: {coursework}")


def scenario_change_status(courseworks: list[Coursework], action: str) -> None:
    """Сдать, вернуть или защитить работу."""
    coursework = ask_coursework(courseworks)
    if coursework is None:
        return
    try:
        if action == "submit":
            coursework.submit()
        elif action == "return":
            coursework.return_to_work()
        elif coursework.status != STATUS_ON_REVIEW:
            raise ValueError("Защитить можно только работу на проверке")
        else:
            coursework.defend(input_int("Оценка (2–5): ", 2, 5))
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    save_courseworks(courseworks)
    print(f"Готово: {coursework}")


def scenario_add_student(students: list[Student]) -> None:
    """Добавить студента."""
    name = input_text("ФИО студента: ")
    group = input_text("Группа: ")
    email = input("Email (можно пропустить): ")
    student = add_student(students, name, group, email)
    save_students(students)
    print(f"Добавлен студент: {student}")


def scenario_add_teacher(teachers: list[Teacher]) -> None:
    """Добавить преподавателя."""
    name = input_text("ФИО преподавателя: ")
    department = input_text("Кафедра: ")
    email = input("Email (можно пропустить): ")
    max_students = input_int("Максимум студентов: ", 1, 30)
    teacher = add_teacher(teachers, name, department, email, max_students)
    save_teachers(teachers)
    print(f"Добавлен преподаватель: {teacher}")


def main() -> None:
    """Точка входа: загрузка данных и главное меню."""
    try:
        students, teachers, courseworks = load_all()
    except ValueError as error:
        print(f"Не удалось загрузить данные: {error}")
        return

    while True:
        print(MENU)
        choice = input_int("Выберите пункт: ", 0, 11)
        print()
        if choice == 0:
            print("До свидания!")
            break
        elif choice == 1:
            show_students(students)
        elif choice == 2:
            show_teachers(teachers, courseworks)
        elif choice == 3:
            show_courseworks(courseworks)
        elif choice == 4:
            show_courseworks(filter_by_status(courseworks, ask_status()))
        elif choice == 5:
            coursework = ask_coursework(courseworks)
            if coursework is not None:
                show_coursework_details(coursework)
        elif choice == 6:
            scenario_create_coursework(students, teachers, courseworks)
        elif choice == 7:
            scenario_change_status(courseworks, "submit")
        elif choice == 8:
            scenario_change_status(courseworks, "return")
        elif choice == 9:
            scenario_change_status(courseworks, "defend")
        elif choice == 10:
            scenario_add_student(students)
        elif choice == 11:
            scenario_add_teacher(teachers)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nРабота программы прервана.")
