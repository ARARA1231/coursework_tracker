from datetime import date

# Данные одной курсовой работы
student_name = "Иван Петров"
student_group = "ИКБО-01-24"
teacher_name = "Смирнова Анна Сергеевна"
teacher_max_students = 5
coursework_title = "Разработка системы учёта курсовых работ"
deadline = date(2026, 12, 20)
status = "в работе"


def can_take_student(current_students, max_students):
    """Проверить, может ли преподаватель взять ещё одного студента."""
    return current_students < max_students


def days_until_deadline(deadline_date):
    """Посчитать, сколько дней осталось до срока сдачи."""
    return (deadline_date - date.today()).days


def get_deadline_message(days_left):
    """Сформировать сообщение о сроке сдачи."""
    if days_left < 0:
        return f"Срок сдачи прошёл {abs(days_left)} дн. назад"
    if days_left == 0:
        return "Сегодня последний день сдачи"
    if days_left <= 7:
        return f"Осталось {days_left} дн. — срок близко!"
    return f"До сдачи осталось {days_left} дн."


def get_status_message(current_status):
    """Вернуть описание статуса курсовой работы."""
    if current_status == "в работе":
        return "Студент выполняет работу"
    elif current_status == "на проверке":
        return "Работа передана руководителю на проверку"
    elif current_status == "защищена":
        return "Работа защищена"
    return "Неизвестный статус"


teacher_current_students = int(input("Сколько студентов уже у руководителя: "))

days_left = days_until_deadline(deadline)

print()
print(f"Курсовая работа: {coursework_title}")
print(f"Студент: {student_name}, группа {student_group}")
print(f"Руководитель: {teacher_name}")
print(f"Срок сдачи: {deadline.strftime('%d.%m.%Y')}")
print(get_deadline_message(days_left))
print(f"Статус: {get_status_message(status)}")

if can_take_student(teacher_current_students, teacher_max_students):
    print("Руководитель может взять ещё одного студента")
else:
    print("У руководителя нет свободных мест")
