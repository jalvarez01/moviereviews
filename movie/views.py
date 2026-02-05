from django.shortcuts import render

def home(request):
    context = {
        'name': 'Juan José'
    }
    return render(request, 'movie/home.html', context)

def about(request):
    return render(request, 'movie/about.html')