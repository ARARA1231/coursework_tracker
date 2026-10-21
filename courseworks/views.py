from django.shortcuts import render

from models.courseworks import find_coursework, sort_by_deadline
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
