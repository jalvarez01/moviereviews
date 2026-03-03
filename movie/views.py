from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import urllib, base64

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Viviana Arango'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>This is an About Page</h1>')
    return render(request, 'about.html')

def statistics_view(request):
    movies = Movie.objects.all()

    # --------- Movies per year ----------
    year_counts = {}
    for m in movies:
        y = m.year if m.year is not None else "Unknown"
        year_counts[y] = year_counts.get(y, 0) + 1

    years = list(year_counts.keys())
    values_year = list(year_counts.values())

    buf1 = io.BytesIO()
    plt.figure()
    plt.bar(range(len(values_year)), values_year)
    plt.title("Movies per year")
    plt.xlabel("Year")
    plt.ylabel("Number of movies")
    plt.xticks(range(len(years)), years, rotation=90)
    plt.tight_layout()
    plt.savefig(buf1, format="png")
    plt.close()
    buf1.seek(0)
    graphic_year = base64.b64encode(buf1.getvalue()).decode("utf-8")
    buf1.close()

    # --------- Movies per genre (first genre) ----------
    genre_counts = {}
    for m in movies:
        g = (m.genre or "").strip()
        first_genre = g.split(",")[0].strip() if g else "Unknown"
        genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    genres = list(genre_counts.keys())
    values_genre = list(genre_counts.values())

    buf2 = io.BytesIO()
    plt.figure()
    plt.bar(range(len(values_genre)), values_genre)
    plt.title("Movies per genre (first genre)")
    plt.xlabel("Genre")
    plt.ylabel("Number of movies")
    plt.xticks(range(len(genres)), genres, rotation=90)
    plt.tight_layout()
    plt.savefig(buf2, format="png")
    plt.close()
    buf2.seek(0)
    graphic_genre = base64.b64encode(buf2.getvalue()).decode("utf-8")
    buf2.close()

    return render(request, "statistics.html", {
        "graphic_year": graphic_year,
        "graphic_genre": graphic_genre,
    })

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})