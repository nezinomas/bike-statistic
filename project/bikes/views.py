from django.shortcuts import render

def index(request):
    return render(
        request,
        'bikes/index.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )
