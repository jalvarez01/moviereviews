from django.core.management.base import BaseCommand
from movie.models import Movie
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        json_file_path = 'movie/management/commands/movies.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)

        # Carga máximo 100 (o menos si el archivo tiene menos)
        limit = min(100, len(movies))

        for i in range(limit):
            movie = movies[i]

            title = (movie.get('title') or '').strip()
            if not title:
                continue  # si no hay título, saltar

            # Algunos datasets traen 'plot', otros 'description'
            plot = movie.get('plot') or movie.get('description') or 'No description available.'
            plot = str(plot).strip()
            if not plot:
                plot = 'No description available.'

            genre = movie.get('genre') or ''
            genre = str(genre).strip()

            year = movie.get('year', None)
            try:
                year = int(year) if year not in (None, '', 'nan') else None
            except (ValueError, TypeError):
                year = None

            exist = Movie.objects.filter(title=title).first()
            if not exist:
                Movie.objects.create(
                    title=title,
                    image='movie/images/default.jpg',
                    genre=genre,
                    year=year,
                    description=plot[:250],  # por tu max_length=250
                )

        self.stdout.write(self.style.SUCCESS(f'Listo: cargadas hasta {limit} películas (sin duplicados).'))        