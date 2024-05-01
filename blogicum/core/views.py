from django.shortcuts import render

from http import HTTPStatus


def csrf_failure(request, reason=''):
    return render(request, 'pages/404.html', status=HTTPStatus.FORBIDDEN)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def server_error(request):
    return render(request, 'pages/500.html')
