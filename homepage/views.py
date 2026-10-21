from django.http import HttpResponse
from django.shortcuts import render


def page(title, content):
    """Общий каркас HTML-страницы: Bootstrap, навигация, контейнер."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav border-bottom mb-4 px-3">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/courseworks/">Курсовые работы</a>
        <a class="nav-link" href="/students/">Студенты</a>
        <a class="nav-link" href="/teachers/">Преподаватели</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание системы и переходы в разделы."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Собственная страница 404 для любого несуществующего адреса."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
