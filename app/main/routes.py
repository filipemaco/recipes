import json

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask import g
from app import db
from app.main.forms import EditProfileForm, RecipeForm, SearchForm
from app.models import User, Recipe, Quantity, Ingredient
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route('/delete_recipe/<id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()
    quantity_set = Quantity.query.filter_by(recipe_id=recipe.id).all()
    for quantity in quantity_set:
        db.session.delete(quantity)
        db.session.commit()

    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for('main.my_recipes'))


@bp.route('', methods=['GET'])
@bp.route('/my_recipes', methods=['GET'])
@login_required
def my_recipes():
    recipes = Recipe.query.filter_by(author=current_user).order_by(Recipe.name).all()

    return render_template(
        'recipes.html',
        recipes=recipes,
        my_recipes=True,
        recipe_url="main:my_recipes"
    )


@bp.route('/all_recipes', methods=['GET'])
@login_required
def all_recipes():
    recipes = Recipe.query.order_by(Recipe.name).all()
    return render_template(
        'recipes.html',
        recipes=recipes,
        all_recipes=True,
        recipe_url="main:all_recipes"
    )


@bp.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    recipe_form = RecipeForm()
    if recipe_form.validate_on_submit():
        recipe_name = recipe_form.name.data

        if Recipe.query.filter_by(author=current_user, name=recipe_name).count():
            return render_template(
                'add_recipes.html',
                title='Home',
                recipe_form=recipe_form,
                recipe_name_repitition=True
            )

        recipe = Recipe(
            name=recipe_name,
            author=current_user
        )

        db.session.add(recipe)
        db.session.commit()

        for ingredient in recipe_form.ingredients.data:
            if not ingredient['value']:
                continue

            # Confirm if ingredient exist

            ingredient = Quantity(
                value=ingredient['value'],
                recipe=recipe,
                ingredient_name=ingredient['ingredient_name'],
                unit_type=ingredient['unit_type'],
            )

            db.session.add(ingredient)
            db.session.commit()

        return redirect(url_for('main.my_recipes'))

    return render_template(
        'add_recipes.html',
        title='Home',
        recipe_form=recipe_form,
        add_recipe=True,
    )


@bp.route('/edit_recipe/<id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()
    recipe_form = RecipeForm()

    if recipe_form.validate_on_submit():
        recipe_name = recipe_form.name.data

        if Recipe.query.filter(Recipe.author == current_user, Recipe.name == recipe_name, Recipe.id != id).count():
            return render_template(
                'add_recipes.html',
                title='Home',
                recipe_form=recipe_form,
                recipe_name_repitition=True
            )

        recipe.name = recipe_name

        db.session.add(recipe)
        db.session.commit()

        quantity_set = Quantity.query.filter_by(recipe_id=recipe.id).all()
        for quantity in quantity_set:
            db.session.delete(quantity)
            db.session.commit()

        for ingredient in recipe_form.ingredients.data:
            if not ingredient['value']:
                continue

            # Confirm if ingredient exist
            ingredient = Quantity(
                value=ingredient['value'],
                recipe=recipe,
                ingredient_name=ingredient['ingredient_name'],
                unit_type=ingredient['unit_type'],
            )
            db.session.add(ingredient)
            db.session.commit()

        return redirect(url_for('main.my_recipes'))

    recipe_form.name.data = recipe.name

    return render_template(
        'add_recipes.html',
        title='Home',
        recipe_form=recipe_form,
        ingredients=recipe.quantity,
        edit_recipe=True,
    )


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/search/<url_to_redirect>')
@login_required
def search(url_to_redirect):
    if not g.search_form.validate():
        return redirect(url_for(url_to_redirect))
    page = request.args.get('page', 1, type=int)
    recipes, total = Recipe.search(g.search_form.q.data, page, 1000)

    if 'my_recipes' in url_to_redirect:
        recipes = recipes.filter_by(author=current_user).order_by(Recipe.name).all()
        return render_template(
            'recipes.html',
            recipes=recipes,
            my_recipes=True,
            recipe_url="main:my_recipes"
        )

    recipes = recipes.order_by(Recipe.name).all()
    return render_template(
        'recipes.html',
        recipes=recipes,
        all_recipes=True,
        recipe_url="main:all_recipes"
    )
