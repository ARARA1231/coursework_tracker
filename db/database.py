import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "coursetrack.sqlite"


def get_connection():
    """Соединение с SQLite: проверка внешних ключей и поля по именам."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all(sql, params=()):
    """Выполнить SELECT и вернуть все строки результата."""
    conn = get_connection()
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def fetch_one(sql, params=()):
    """Выполнить SELECT и вернуть одну строку (или None)."""
    conn = get_connection()
    try:
        return conn.execute(sql, params).fetchone()
    finally:
        conn.close()
