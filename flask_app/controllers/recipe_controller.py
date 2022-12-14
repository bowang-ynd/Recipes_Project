from flask import render_template, request, redirect, flash, session
from flask_app import app, bcrypt

from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

#? ==================== USER PAGE after LOGIN ====================
@app.route('/recipes')
def welcome():
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')

    user = User.get_by_id({'id' : session['uid']})
    recipes = Recipe.get_all()

    return render_template('recipes.html', user=user, recipes=recipes)

#? ==================== CREATE ONE Recipe ====================
@app.route('/create_recipe')
def direct_to_new_recipe():
    if 'uid' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/create_recipe_process', methods=["POST"])
def create_recipe():
    if 'uid' not in session:
        return redirect('/')

    # checks valid input
    is_valid = Recipe.validate_recipe(request.form)
    if not is_valid:
        return redirect('/create_recipe')

    data = {
        **request.form,
        'owner_id' : session['uid']
    }

    Recipe.create(data)

    return redirect('/recipes')

#? ==================== READ ONE RECIPE ====================
@app.route('/recipes/<int:recipe_id>')
def show_one_recipe(recipe_id):
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')
    user = User.get_by_id({'id' : session['uid']})
    recipe = Recipe.get_one_recipe({'id' : recipe_id})

    return render_template('one_recipe.html', user=user, recipe=recipe)

#? ==================== UPDATE ONE RECIPE ====================
@app.route('/recipes/edit/<int:recipe_id>')
def direct_to_edit(recipe_id):
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')
    
    return render_template('edit_recipe.html', recipe_id=recipe_id)

@app.route('/edit_recipe_process', methods=["POST"])
def edit_one_recipe():
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')

    # checks valid input
    is_valid = Recipe.validate_recipe(request.form)
    if not is_valid:
        id = request.form['id']
        return redirect(f'/recipes/edit/{id}')

    Recipe.edit_recipe_with_id(request.form)
    return redirect('/recipes')

#? ==================== DELETE ONE RECIPE ====================
@app.route('/recipes/delete/<int:recipe_id>')
def delete_one_recipe(recipe_id):

    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')
    
    data = {
        'id' : recipe_id
    }
    
    # prevent other users to delete
    recipe = Recipe.get_one_recipe()
    if session['uid'] != recipe.owner_id:
        return redirect('/recipes')

    # now delete the recipe 
    Recipe.delete_recipe_with_id(data)

    return redirect('/recipes')


