from django.shortcuts import render
from .models import Movie
from .models import Movie

def home(request):
    context = {
        'name': 'Juan José'
    }
    return render(request, 'movie/home.html', context)

def about(request):
    return render(request, 'movie/about.html')

def movie_list(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movie/movie_list.html', {'movies': movies})