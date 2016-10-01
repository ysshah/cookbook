from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    LOCATIONS = (
        ('pantry', 'Pantry'),
        ('fridge', 'Fridge'),
        ('freezer', 'Freezer')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    purchase_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    location = models.CharField(max_length=10, choices=LOCATIONS)
    class Meta:
        unique_together = ('user', 'name')
    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    class Meta:
        unique_together = ('user', 'name')
    def __str__(self):
        return self.name


class RecipeInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    number = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = ('recipe', 'number')
    def __str__(self):
        return self.text


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    number = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = (('recipe', 'name'),('recipe','number'))
    def __str__(self):
        return self.name


class Lifespan(models.Model):
    ingredient = models.CharField(max_length=200)
    room_temperature = models.PositiveSmallIntegerField(null=True)
    fridge = models.PositiveSmallIntegerField(null=True)
    freezer = models.PositiveSmallIntegerField(null=True)
    def __str__(self):
        return self.ingredient
