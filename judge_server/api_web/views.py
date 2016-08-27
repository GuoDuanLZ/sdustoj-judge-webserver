from django.shortcuts import render


def api_homepage(request):
    return render(request, 'api_homepage.html', {
        'user': request.user
    })
