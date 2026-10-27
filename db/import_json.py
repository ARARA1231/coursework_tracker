import json

from db.database import BASE_DIR, get_connection

DATA_DIR = BASE_DIR / "data"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


def load_json(name):
    with open(DATA_DIR / name, encoding="utf-8") as file:
        return json.load(file)


def create_schema(conn):
    conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))


def clear_tables(conn):
    """Очистка перед повторным импортом (сначала зависимая таблица)."""
    conn.execute("DELETE FROM courseworks")
    conn.execute("DELETE FROM students")
    conn.execute("DELETE FROM teachers")


def import_students(conn):
    conn.executemany(
        "INSERT INTO students (id, name, group_name, email) "
        "VALUES (?, ?, ?, ?)",
        [
            (s["id"], s["name"], s["group"], s["email"])
            for s in load_json("students.json")
        ],
    )


def import_teachers(conn):
    conn.executemany(
        "INSERT INTO teachers (id, name, department, email, max_students) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            (t["id"], t["name"], t["department"], t["email"],
             t["max_students"])
            for t in load_json("teachers.json")
        ],
    )


def import_courseworks(conn):
    conn.executemany(
        "INSERT INTO courseworks "
        "(id, title, student_id, teacher_id, deadline, status, grade) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (c["id"], c["title"], c["student_id"], c["teacher_id"],
             c["deadline"], c["status"], c["grade"])
            for c in load_json("courseworks.json")
        ],
    )


def main():
    conn = get_connection()
    try:
        create_schema(conn)
        clear_tables(conn)
        import_students(conn)
        import_teachers(conn)
        import_courseworks(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("Импорт завершён:", DATA_DIR / "coursetrack.sqlite")


if __name__ == "__main__":
    main()
