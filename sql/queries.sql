-- ==========================================
-- Система учёта курсовых работ: SQL-запросы
-- Проверка: sqlite3 data/coursetrack.sqlite
-- ==========================================

-- Запрос 1. Список студентов, по алфавиту (выборка списка)
SELECT id, name, group_name, email
FROM students
ORDER BY name;

-- Запрос 2. Список преподавателей с лимитом руководства (выборка списка)
SELECT id, name, department, max_students
FROM teachers
ORDER BY name;

-- Запрос 3. Работы с заданным статусом (WHERE)
SELECT id, title, deadline, status
FROM courseworks
WHERE status = 'на проверке'
ORDER BY deadline;

-- Запрос 4. Просроченные незащищённые работы (WHERE, сравнение дат)
SELECT id, title, deadline
FROM courseworks
WHERE status <> 'защищена'
  AND deadline < date('now')
ORDER BY deadline;

-- Запрос 5. Активные работы: название, студент, руководитель (JOIN)
SELECT
    c.id, c.title, c.deadline, c.status,
    s.name AS student_name, s.group_name,
    t.name AS teacher_name
FROM courseworks AS c
JOIN students AS s ON c.student_id = s.id
JOIN teachers AS t ON c.teacher_id = t.id
WHERE c.status IN ('в работе', 'на проверке')
ORDER BY c.deadline;

-- Запрос 6. Защищённые работы с оценкой и фамилией студента (JOIN)
SELECT c.title, s.name AS student_name, c.grade
FROM courseworks AS c
JOIN students AS s ON c.student_id = s.id
WHERE c.status = 'защищена';

-- Запрос 7. Преподаватели, у которых есть свободные места
--           (LEFT JOIN, COUNT, GROUP BY, HAVING)
SELECT
    t.id, t.name, t.department, t.max_students,
    COUNT(c.id) AS active_count,
    t.max_students - COUNT(c.id) AS free_slots
FROM teachers AS t
LEFT JOIN courseworks AS c
    ON c.teacher_id = t.id AND c.status IN ('в работе', 'на проверке')
GROUP BY t.id
HAVING free_slots > 0
ORDER BY free_slots DESC;

-- Запрос 8. Общее количество работ, защищённых и средняя оценка (агрегаты)
SELECT
    COUNT(*) AS total,
    SUM(status = 'защищена') AS defended,
    ROUND(AVG(grade), 2) AS avg_grade
FROM courseworks;

-- Запрос 9. Количество работ по статусам (COUNT + GROUP BY)
SELECT status, COUNT(*) AS cnt
FROM courseworks
GROUP BY status
ORDER BY cnt DESC;

-- Запрос 10. Количество работ у каждого преподавателя (JOIN + GROUP BY)
SELECT t.name, t.max_students, COUNT(c.id) AS cnt
FROM teachers AS t
LEFT JOIN courseworks AS c ON c.teacher_id = t.id
GROUP BY t.id
ORDER BY cnt DESC, t.name;

-- Запрос 11. Студенты, у которых ещё нет курсовой работы (LEFT JOIN)
SELECT s.id, s.name, s.group_name
FROM students AS s
LEFT JOIN courseworks AS c ON c.student_id = s.id
WHERE c.id IS NULL
ORDER BY s.name;

-- Запрос 12. Количество студентов в каждой группе (COUNT + GROUP BY)
SELECT group_name, COUNT(*) AS cnt
FROM students
GROUP BY group_name
ORDER BY group_name;
