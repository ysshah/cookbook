# Cookbook

A Django app used for tracking your ingredients to determine which recipes you can make, and how many days you have left to make them. Very pre-alpha. I'm quite new to Django so any help would be greatly appreciated.

## How it works

First, you enter in your ingredients and recipes. The left column shows you your ingredients along with how many days you have left to use them. The middle column shows you your recipes and whether you can make them or not - if you can make them, it also shows how many days you have left to make them (until the first ingredient expires). Finally, clicking on a recipe lets you view its details in the right column, and shows you which of its ingredients you have and which are missing.

## Models

`Ingredient` - User ingredients

`Recipe` - User recipes

`RecipeIngredient` and `RecipeInstruction` - Ingredients and instructions for each recipe (for each user)

`Lifespan` - How many days ingredients can last depending on where they are stored (room temperature, fridge, or freezer)

## Todo

#### Easy

* Change username / password
* Display fraction of ingredients available
* Optional ingredients in recipes
* Keyboard shortcuts
* Comment and clean up code
* Better application name that's not already taken

#### More difficult

* Combine the migrations into one
* Clean up UI, make prettier
* Download recipes from popular sites by entering URL
* Custom ingredient locations
* "Remember me" option when logging in
* Search for ingredients and recipes
* Edit / delete multiple recipes
* Edit / delete multiple ingredients
* Incorporate ingredient purchase date
* Ingredient quantities in recipes
* Multiple variations of same ingredient
  * Alfredo sauce, marinara sauce, etc.
* Grocery list generator
* Option to hide items without required ingredients
* Create a mobile view

#### Optional

* Use Django forms instead of manually creating them

## Contribute

Clone the repository, install the dependencies, migrate the models, and load the fixtures (or enter in your own ingredients and recipes). You can make whatever improvements you would like - I will be extremely grateful for any pull requests. Thank you!
