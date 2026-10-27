import sqlite3

import pytest

from db import import_json, queries
from db.database import fetch_all


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Импорт JSON во временную базу, чтобы не трогать рабочую."""
    path = tmp_path / "test.sqlite"
    monkeypatch.setattr("db.database.DB_PATH", path)
    import_json.main()
    return path


def test_tables_created(temp_db):
    conn = sqlite3.connect(temp_db)
    names = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert {"students", "teachers", "courseworks"} <= names


def test_import_counts(temp_db):
    assert len(fetch_all(queries.STUDENT_LIST)) == 7
    assert fetch_all(queries.TOTALS)[0]["total"] == 6


def test_reimport_does_not_duplicate(temp_db):
    import_json.main()
    assert fetch_all(queries.TOTALS)[0]["total"] == 6


def test_foreign_key_enforced(temp_db):
    from db.database import get_connection
    conn = get_connection()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO courseworks (title, student_id, teacher_id, "
            "deadline) VALUES ('x', 999, 1, '2026-12-01')")
    conn.close()


def test_free_teachers_excludes_full(temp_db):
    rows = fetch_all(queries.FREE_TEACHERS, ("%", 1))
    names = [r["name"] for r in rows]
    assert all(r["free_slots"] >= 1 for r in rows)
    assert not any(n.startswith("Орлова") for n in names)


def test_students_without_work(temp_db):
    rows = fetch_all(queries.STUDENTS_WITHOUT_WORK)
    assert [r["name"] for r in rows] == ["Артём Васильев"]
