from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import logout

from .models import *


def getContext(request):
    if request.user.is_authenticated():
        today = date.today()

        daysRemainingDict = {}

        ingredients = Ingredient.objects.filter(user=request.user)
        for ingredient in ingredients:
            days_remaining = ''
            if ingredient.expiration_date:
                days_remaining = (ingredient.expiration_date - today).days + 1
            elif ingredient.purchase_date and Lifespan.objects.filter(ingredient=ingredient.name).exists():
                life = Lifespan.objects.get(ingredient=ingredient.name)
                if ingredient.location == 'Pantry':
                    if life.room_temperature:
                        days_remaining = (ingredient.purchase_date + timedelta(days=life.room_temperature) - today).days + 1
                elif ingredient.location == 'Fridge':
                    if life.fridge:
                        days_remaining = (ingredient.purchase_date + timedelta(days=life.fridge) - today).days + 1
                elif ingredient.location == 'Freezer':
                    if life.freezer:
                        days_remaining = (ingredient.purchase_date + timedelta(days=life.freezer) - today).days + 1
            if days_remaining != '':
                daysRemainingDict[ingredient.name] = days_remaining
                ingredient.days_remaining = days_remaining

        ingredientNames = ingredients.values_list('name', flat=True)
        recipes = Recipe.objects.filter(user=request.user)
        for recipe in recipes:
            recipeIngredients = RecipeIngredient.objects.filter(
                recipe=recipe).order_by('number')
            if recipeIngredients.exists():
                daysRemainingList = []
                numIngredientsMissing = 0
                for recipeIngredient in recipeIngredients:
                    if recipeIngredient.name in ingredientNames:
                        recipeIngredient.able = 'yes'
                        if recipeIngredient.name in daysRemainingDict:
                            days_remaining = daysRemainingDict[recipeIngredient.name]
                            recipeIngredient.days_remaining = days_remaining
                            daysRemainingList.append(days_remaining)
                    else:
                        recipeIngredient.able = 'no'
                        numIngredientsMissing += 1

                recipe.ingredients = recipeIngredients
                if numIngredientsMissing == 0:
                    recipe.able = 'yes'
                    if daysRemainingList:
                        recipe.days_remaining = min(daysRemainingList)
                else:
                    recipe.able = 'no'
            else:
                if Ingredient.objects.filter(name__iexact=recipe.name).exists():
                    thisIngredient = Ingredient.objects.get(name__iexact=recipe.name)
                    recipe.able = 'yes'
                    if thisIngredient.name in daysRemainingDict:
                        recipe.days_remaining = daysRemainingDict[thisIngredient.name]
                else:
                    recipe.able = 'no'

        recipe.instructions = RecipeInstruction.objects.filter(
            recipe=recipe).order_by('number')
        locations = [loc[1] for loc in Ingredient.LOCATIONS]

        context = {
            'recipes': recipes,
            'ingredients': ingredients,
            'locations': locations,
            'newRecipeModal': True
        }
        return context
    else:
        return {}


def index(request):
    return render(request, 'index.html', getContext(request))


def logUserOut(request):
    logout(request)
    return redirect('/')


def reloadContent(request):
    return render(request, 'content.html', getContext(request))


def loadRecipeModal(request):
    if request.is_ajax() and request.POST and request.user.is_authenticated():
        pk = request.POST['id']
        if Recipe.objects.filter(pk=pk, user=request.user).exists():
            recipe = Recipe.objects.get(pk=pk, user=request.user)
            context = {
                'newRecipeModal': False,
                'recipe': recipe,
                'ingredients': RecipeIngredient.objects.filter(
                    recipe=recipe).order_by('number'),
                'instructions': RecipeInstruction.objects.filter(
                    recipe=recipe).order_by('number')
            }
        else:
            context = { 'newRecipeModal': True }
        return render(request, 'recipeModal.html', context)
    else:
        raise Http404
