from django.http import HttpResponse

from homepage.views import page
from models.courseworks import (
    count_active_for_teacher,
    get_teacher_courseworks,
)
from models.teachers import find_teacher, sort_teachers
from storage import load_all


def teacher_list(request):
    """Список преподавателей с занятостью."""
    _, teachers, courseworks = load_all()
    items = ""
    for teacher in sort_teachers(teachers):
        active = count_active_for_teacher(courseworks, teacher)
        items += f"""
        <li class="list-group-item">
            <a href="/teachers/{teacher.id}/">{teacher.name}</a>
            <span class="text-muted">— {teacher.department},
            занято {active} из {teacher.max_students}</span>
        </li>"""
    content = f"""
    <h1>Преподаватели</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Преподаватели", content))


def teacher_detail(request, teacher_id):
    """Карточка преподавателя и работы под его руководством."""
    _, teachers, courseworks = load_all()
    teacher = find_teacher(teachers, teacher_id)
    if teacher is None:
        content = """
        <h1>Преподаватель не найден</h1>
        <a href="/teachers/" class="btn btn-secondary">К списку</a>
        """
        return HttpResponse(
            page("Преподаватель не найден", content), status=404
        )

    active = count_active_for_teacher(courseworks, teacher)
    if teacher.has_free_slots(active):
        badge = '<span class="badge bg-success">Есть свободные места</span>'
    else:
        badge = '<span class="badge bg-danger">Мест нет</span>'

    works = ""
    for coursework in get_teacher_courseworks(courseworks, teacher):
        works += f"""
        <li class="list-group-item">
            <a href="/courseworks/{coursework.id}/">{coursework.title}</a>
            — {coursework.student.name}, {coursework.status}
        </li>"""
    if not works:
        works = '<li class="list-group-item">Работ пока нет</li>'

    content = f"""
    <h1>{teacher.name}</h1>
    <p>Кафедра: {teacher.department}</p>
    <p>Занято {active} из {teacher.max_students} {badge}</p>
    <h2 class="h5">Курсовые работы</h2>
    <ul class="list-group mb-3">{works}</ul>
    <a href="/teachers/" class="btn btn-secondary">К списку</a>
    """
    return HttpResponse(page(teacher.name, content))
