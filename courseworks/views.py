from django.http import HttpResponse

from homepage.views import page
from models.courseworks import find_coursework, sort_by_deadline
from storage import load_all


def coursework_list(request):
    """Список курсовых работ по сроку сдачи."""
    _, _, courseworks = load_all()
    items = ""
    for coursework in sort_by_deadline(courseworks):
        items += f"""
        <li class="list-group-item">
            <a href="/courseworks/{coursework.id}/">{coursework.title}</a>
            <span class="text-muted">— {coursework.student.name},
            срок {coursework.deadline.strftime('%d.%m.%Y')},
            {coursework.status}</span>
        </li>"""
    content = f"""
    <h1>Курсовые работы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Курсовые работы", content))


def coursework_detail(request, coursework_id):
    """Подробная информация о курсовой работе."""
    _, _, courseworks = load_all()
    coursework = find_coursework(courseworks, coursework_id)
    if coursework is None:
        content = """
        <h1>Курсовая работа не найдена</h1>
        <a href="/courseworks/" class="btn btn-secondary">К списку</a>
        """
        return HttpResponse(
            page("Работа не найдена", content), status=404
        )

    grade = coursework.grade if coursework.grade else "не выставлена"
    content = f"""
    <h1>{coursework.title}</h1>
    <p>Студент: {coursework.student.name}, {coursework.student.group}</p>
    <p>Руководитель: {coursework.teacher.name}</p>
    <p>Срок сдачи: {coursework.deadline.strftime('%d.%m.%Y')}
       — {coursework.deadline_message}</p>
    <p>Статус: {coursework.status} ({coursework.status_message})</p>
    <p>Оценка: {grade}</p>
    <a href="/courseworks/" class="btn btn-secondary">К списку работ</a>
    """
    return HttpResponse(page(coursework.title, content))
