-- ==========================================
-- Система учёта курсовых работ: структура БД
-- ==========================================

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT NOT NULL,
    max_students INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS courseworks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    student_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    deadline TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'в работе',
    grade INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);
