from django.http import HttpResponse

from homepage.views import page
from models.courseworks import get_student_courseworks
from models.students import find_student, sort_students
from storage import load_all


def student_list(request):
    """Список всех студентов."""
    students, _, _ = load_all()
    items = ""
    for student in sort_students(students):
        items += f"""
        <li class="list-group-item">
            <a href="/students/{student.id}/">{student.name}</a>
            <span class="text-muted">— {student.group}</span>
        </li>"""
    content = f"""
    <h1>Студенты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Студенты", content))


def student_detail(request, student_id):
    """Карточка студента и его курсовые работы."""
    students, _, courseworks = load_all()
    student = find_student(students, student_id)
    if student is None:
        content = """
        <h1>Студент не найден</h1>
        <a href="/students/" class="btn btn-secondary">К списку</a>
        """
        return HttpResponse(page("Студент не найден", content), status=404)

    works = ""
    for coursework in get_student_courseworks(courseworks, student):
        works += f"""
        <li class="list-group-item">
            <a href="/courseworks/{coursework.id}/">{coursework.title}</a>
            — {coursework.status}
        </li>"""
    if not works:
        works = '<li class="list-group-item">Курсовой работы пока нет</li>'

    content = f"""
    <h1>{student.name}</h1>
    <p>Группа: {student.group}</p>
    <p>Email: {student.email}</p>
    <h2 class="h5">Курсовые работы</h2>
    <ul class="list-group mb-3">{works}</ul>
    <a href="/students/" class="btn btn-secondary">К списку студентов</a>
    """
    return HttpResponse(page(student.name, content))
