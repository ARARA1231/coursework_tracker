"""Вспомогательные функции безопасного ввода."""

from datetime import date, datetime


def input_int(
    prompt: str,
    min_value: int | None = None,
    max_value: int | None = None,
) -> int:
    """Запрашивать целое число, пока пользователь не введёт корректное."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Нужно ввести целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"Число должно быть не меньше {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Число должно быть не больше {max_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запрашивать дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            print("Формат даты: ДД.ММ.ГГГГ, например 20.12.2026.")


def input_text(prompt: str) -> str:
    """Запрашивать непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не может быть пустым.")
