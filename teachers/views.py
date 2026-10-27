from django.shortcuts import render

from db import queries
from db.database import fetch_all

from models.courseworks import (
    count_active_for_teacher,
    get_teacher_courseworks,
    sort_by_deadline,
)
from models.teachers import find_teacher, sort_teachers
from storage import load_all


def teacher_list(request):
    """Список преподавателей с занятостью."""
    _, teachers, courseworks = load_all()
    teacher_rows = []
    for teacher in sort_teachers(teachers):
        active_count = count_active_for_teacher(courseworks, teacher)
        teacher_rows.append({
            "teacher": teacher,
            "active_count": active_count,
            "free_slots": teacher.free_slots(active_count),
        })
    context = {"teacher_rows": teacher_rows}
    return render(request, "teachers/teacher_list.html", context)


def teacher_detail(request, teacher_id):
    """Карточка преподавателя и работы под его руководством."""
    _, teachers, courseworks = load_all()
    teacher = find_teacher(teachers, teacher_id)
    context = {"teacher": teacher}
    if teacher is not None:
        active_count = count_active_for_teacher(courseworks, teacher)
        context.update({
            "courseworks": sort_by_deadline(
                get_teacher_courseworks(courseworks, teacher)
            ),
            "active_count": active_count,
            "free_slots": teacher.free_slots(active_count),
        })
    return render(
        request,
        "teachers/teacher_detail.html",
        context,
        status=404 if teacher is None else 200,
    )


def free_teachers(request):
    """Поиск руководителя: свободные места и фильтр по кафедре (ПР7)."""
    department = request.GET.get("department", "")
    try:
        min_slots = max(1, int(request.GET.get("min_slots", 1)))
    except ValueError:
        min_slots = 1
    rows = fetch_all(
        queries.FREE_TEACHERS, (f"%{department}%", min_slots)
    )
    context = {
        "teachers": rows,
        "departments": [
            row["department"] for row in fetch_all(queries.DEPARTMENTS)
        ],
        "department": department,
        "min_slots": min_slots,
    }
    return render(request, "teachers/free.html", context)
