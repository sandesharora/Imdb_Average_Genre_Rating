from django.db import models

# Create your models here.


class movie_data(models.Model):
    movie_name = models.CharField(max_length=100)
    movie_rating = models.DecimalField(max_digits=10,decimal_places=2)
    movie_genre = models.CharField(max_length=20)

