from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_year = models.IntegerField()
    image = models.ImageField(upload_to='movies/', null=True, blank=True)

    def __str__(self):
        return self.title