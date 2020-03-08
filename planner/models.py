from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255, unique=False)
    instructions = models.TextField()
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=False)
    amount = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
