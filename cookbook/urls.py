from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^reloadContent$', views.reloadContent, name='reloadContent'),
    url(r'^loadRecipeModal$', views.loadRecipeModal, name='loadRecipeModal'),

    url(r'^login$', ajax.logUserIn, name='login'),
    url(r'^logout$', views.logUserOut, name='logout'),
    url(r'^createUser$', ajax.createUser, name='createUser'),

    url(r'^addIngredient$', ajax.addIngredient, name='addIngredient'),
    url(r'^updateIngredient$', ajax.updateIngredient, name='updateIngredient'),
    url(r'^deleteIngredient$', ajax.deleteIngredient, name='deleteIngredient'),
    url(r'^addRecipe$', ajax.addRecipe, name='addRecipe'),
    url(r'^updateRecipe$', ajax.updateRecipe, name='updateRecipe'),
    url(r'^deleteRecipe$', ajax.deleteRecipe, name='deleteRecipe')
]
