from django.shortcuts import render

from db import queries
from db.database import fetch_all, fetch_one
from models.courseworks import (
    STATUS_DEFENDED,
    STATUS_IN_PROGRESS,
    STATUS_ON_REVIEW,
    find_coursework,
    sort_by_deadline,
)
from storage import load_all


def coursework_list(request):
    """Список курсовых работ, отсортированный по сроку сдачи."""
    _, _, courseworks = load_all()
    context = {"courseworks": sort_by_deadline(courseworks)}
    return render(request, "courseworks/coursework_list.html", context)


def coursework_detail(request, coursework_id):
    """Подробная информация о курсовой работе."""
    _, _, courseworks = load_all()
    coursework = find_coursework(courseworks, coursework_id)
    context = {"coursework": coursework}
    return render(
        request,
        "courseworks/coursework_detail.html",
        context,
        status=404 if coursework is None else 200,
    )


# ---------- ПР7: страницы на данных из SQLite ----------

def active_courseworks(request):
    """Активные работы: данные трёх таблиц через JOIN."""
    rows = fetch_all(queries.ACTIVE_COURSEWORKS)
    return render(
        request, "courseworks/active.html", {"courseworks": rows}
    )


def by_status(request):
    """Работы с выбранным статусом (WHERE с параметром)."""
    status = request.GET.get("status", STATUS_IN_PROGRESS)
    rows = fetch_all(queries.COURSEWORKS_BY_STATUS, (status,))
    context = {
        "status": status,
        "statuses": [STATUS_IN_PROGRESS, STATUS_ON_REVIEW, STATUS_DEFENDED],
        "courseworks": rows,
    }
    return render(request, "courseworks/by_status.html", context)


def statistics(request):
    """Статистика: агрегатные функции и группировка."""
    context = {
        "totals": fetch_one(queries.TOTALS),
        "by_status": fetch_all(queries.BY_STATUS),
        "by_teacher": fetch_all(queries.BY_TEACHER),
        "without_work": fetch_all(queries.STUDENTS_WITHOUT_WORK),
    }
    return render(request, "courseworks/statistics.html", context)
