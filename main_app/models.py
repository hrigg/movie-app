from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    name= models.CharField(max_length=100)
    image= models.CharField(max_length=250)
    year= models.IntegerField(default=2022)
    description= models.TextField(max_length=500)
    created_at= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name

    class Meta:
        ordering= ['name']

class Review(models.Model):
    title= models.CharField(max_length=100)
    rating= models.IntegerField(default=100, 
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    reason= models.TextField(max_length=1000)
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.title

    class Meta:
        ordering= ['title']

class List(models.Model):
    title=models.CharField(max_length=150)
    movies= models.ManyToManyField(Movie)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.title