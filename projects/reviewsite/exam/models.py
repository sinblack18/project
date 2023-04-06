from django.db import models
from django.utils import timezone

# Create your models here.


class Movie(models.Model):
    genre = models.CharField(max_length=20)
    movie_name = models.CharField(max_length=100)
    movie_summary = models.TextField(max_length=5000)
    reg_date = models.DateTimeField(default=timezone.now)


class Review(models.Model):
    reviewer_name = models.CharField(max_length=20, default='익명의 관객')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=5000)
    score = models.IntegerField(default=0)
    reg_date = models.DateTimeField(default=timezone.now)
