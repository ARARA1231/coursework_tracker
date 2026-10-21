from django.shortcuts import render

from models.courseworks import get_student_courseworks
from models.students import find_student, sort_students
from storage import load_all


def student_list(request):
    """Список всех студентов."""
    students, _, _ = load_all()
    context = {"students": sort_students(students)}
    return render(request, "students/student_list.html", context)


def student_detail(request, student_id):
    """Карточка студента и его курсовые работы."""
    students, _, courseworks = load_all()
    student = find_student(students, student_id)
    context = {
        "student": student,
        "courseworks": (
            get_student_courseworks(courseworks, student) if student else []
        ),
    }
    return render(
        request,
        "students/student_detail.html",
        context,
        status=404 if student is None else 200,
    )
