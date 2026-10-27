"""SQL-запросы, которые используют Django-представления.

Тексты совпадают с запросами из sql/queries.sql (номера в комментариях).
"""

ACTIVE = "('в работе', 'на проверке')"

# Запрос 1. Список студентов с группой (SELECT + ORDER BY)
STUDENT_LIST = """
SELECT id, name, group_name, email
FROM students
ORDER BY name
"""

# Запрос 3. Работы с выбранным статусом (WHERE + параметр)
COURSEWORKS_BY_STATUS = """
SELECT id, title, deadline, status
FROM courseworks
WHERE status = ?
ORDER BY deadline
"""

# Запрос 5. Активные работы со студентом и руководителем (JOIN + WHERE)
ACTIVE_COURSEWORKS = f"""
SELECT
    c.id, c.title, c.deadline, c.status,
    s.name AS student_name, s.group_name,
    t.name AS teacher_name,
    c.deadline < date('now') AS is_overdue
FROM courseworks AS c
JOIN students AS s ON c.student_id = s.id
JOIN teachers AS t ON c.teacher_id = t.id
WHERE c.status IN {ACTIVE}
ORDER BY c.deadline
"""

# Запрос 7. Преподаватели со свободными местами (LEFT JOIN + GROUP BY +
# HAVING), с необязательным фильтром по кафедре
FREE_TEACHERS = f"""
SELECT
    t.id, t.name, t.department, t.max_students,
    COUNT(c.id) AS active_count,
    t.max_students - COUNT(c.id) AS free_slots
FROM teachers AS t
LEFT JOIN courseworks AS c
    ON c.teacher_id = t.id AND c.status IN {ACTIVE}
WHERE t.department LIKE ?
GROUP BY t.id
HAVING free_slots >= ?
ORDER BY free_slots DESC, t.name
"""

DEPARTMENTS = """
SELECT DISTINCT department FROM teachers ORDER BY department
"""

# Запрос 8. Общее количество работ и средняя оценка (агрегаты)
TOTALS = """
SELECT
    COUNT(*) AS total,
    SUM(status = 'защищена') AS defended,
    ROUND(AVG(grade), 2) AS avg_grade
FROM courseworks
"""

# Запрос 9. Количество работ по статусам (GROUP BY)
BY_STATUS = """
SELECT status, COUNT(*) AS cnt
FROM courseworks
GROUP BY status
ORDER BY cnt DESC
"""

# Запрос 10. Нагрузка по преподавателям (JOIN + GROUP BY)
BY_TEACHER = """
SELECT t.name, t.max_students, COUNT(c.id) AS cnt
FROM teachers AS t
LEFT JOIN courseworks AS c ON c.teacher_id = t.id
GROUP BY t.id
ORDER BY cnt DESC, t.name
"""

# Запрос 11. Студенты без курсовой работы (LEFT JOIN + IS NULL)
STUDENTS_WITHOUT_WORK = """
SELECT s.id, s.name, s.group_name
FROM students AS s
LEFT JOIN courseworks AS c ON c.student_id = s.id
WHERE c.id IS NULL
ORDER BY s.name
"""
