import json
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .models import *


def makeNoneIfEmpty(x):
    return x if x else None


def addIngredient(request):
    if request.is_ajax() and request.POST and request.user.is_authenticated():
        name = request.POST['name']
        if Ingredient.objects.filter(name=name, user=request.user).exists():
            msg = 'Error: Ingredient already exists.'.format(name)
            code = 0
        else:
            Ingredient(name=name,
                purchase_date=makeNoneIfEmpty(request.POST['purchase']),
                expiration_date=makeNoneIfEmpty(request.POST['expiration']),
                location=makeNoneIfEmpty(request.POST['location']),
                user=request.user).save()
            msg = 'Ingredient {} added.'.format(name)
            code = 1

        data = json.dumps({ 'code': code, 'message': msg })
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def updateIngredient(request):
    if request.is_ajax() and request.POST and request.user.is_authenticated():
        pk = request.POST['id']
        if Ingredient.objects.filter(pk=pk, user=request.user).exists():
            i = Ingredient.objects.get(pk=pk, user=request.user)
            i.name = request.POST['name']
            i.purchase_date = makeNoneIfEmpty(request.POST['purchase'])
            i.expiration_date = makeNoneIfEmpty(request.POST['expiration'])
            i.location = makeNoneIfEmpty(request.POST['location'])
            i.save()
            msg = 'Ingredient successfully updated.'
            code = 1
        else:
            msg = 'Error: Ingredient does not exist.'
            code = 0

        data = json.dumps({ 'code': code, 'message': msg })
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def deleteIngredient(request):
    if request.is_ajax() and request.POST and request.user.is_authenticated():
        pk = request.POST['id']
        if Ingredient.objects.filter(pk=pk, user=request.user).exists():
            Ingredient.objects.get(pk=pk, user=request.user).delete()
            code = 1
            msg = 'Ingredient deleted.'
        else:
            code = 0
            msg = 'Error: Unable to delete ingredient.'
        data = json.dumps({'code': code, 'message': msg})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def addRecipe(request):
    if request.is_ajax() and request.POST and request.user.is_authenticated():
        name = request.POST['name']
        if Recipe.objects.filter(name=name, user=request.user).exists():
            msg = 'Error: Recipe {} exists'.format(name)
            code = 0
        else:
            newRecipe = Recipe(name=name, user=request.user)
            newRecipe.save()
            for i, instruction in enumerate(request.POST.getlist('instArray[]')):
                RecipeInstruction(text=instruction, number=i,
                    recipe=newRecipe).save()
            for i, ingredient in enumerate(request.POST.getlist('ingrArray[]')):
                RecipeIngredient(name=ingredient, number=i,
                    recipe=newRecipe).save()
            msg = 'Recipe {} added'.format(name)
            code = 1

        data = json.dumps({ 'message': msg, 'code': code })
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def updateRecipe(request):
    if request.is_ajax() and request.POST and request.user.is_authenticated():
        pk = request.POST['id']
        if Recipe.objects.filter(pk=pk, user=request.user).exists():
            r = Recipe.objects.get(pk=pk, user=request.user)
            r.name = request.POST['name']
            r.save()
            for i, instruction in enumerate(request.POST.getlist('instArray[]')):
                RecipeInstruction.objects.update_or_create(recipe=r, number=i,
                    defaults={'text': instruction})
            RecipeInstruction.objects.filter(recipe=r, number__gt=i).delete()
            for i, ingredient in enumerate(request.POST.getlist('ingrArray[]')):
                RecipeIngredient.objects.update_or_create(recipe=r, number=i,
                    defaults={'name': ingredient})
            RecipeIngredient.objects.filter(recipe=r, number__gt=i).delete()
            msg = 'Recipe successfully updated.'
            code = 1
        else:
            msg = 'Error: Recipe does not exist.'
            code = 0

        data = json.dumps({ 'message': msg, 'code': code })
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def deleteRecipe(request):
    if request.is_ajax() and request.POST and request.user.is_authenticated():
        pk = request.POST['id']
        if Recipe.objects.filter(pk=pk, user=request.user).exists():
            Recipe.objects.get(pk=pk, user=request.user).delete()
            msg = 'Recipe deleted.'
            code = 1
        else:
            msg = 'Error: Unable to delete recipe.'
            code = 0
        data = json.dumps({ 'message': msg, 'code': code })
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def logUserIn(request):
    if request.is_ajax() and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data = json.dumps({'code': 1})
        else:
            data = json.dumps({'code': 0})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
