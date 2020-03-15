import json

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, RecipeForm
from app.models import User, Recipe, Quantity, Ingredient
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    recipe_form = RecipeForm()
    if recipe_form.validate_on_submit():
        recipe_name = recipe_form.name.data

        recipe = Recipe(
            name=recipe_name,
            author=current_user
        )

        # db.session.add(recipe)
        # db.session.commit()

        for ingredient in recipe_form.ingredients.data:
            if not ingredient['value']:
                continue

            # Confirm if ingredient exist

            # ingredient = Ingredient.query.filter(Ingredient.name == ingredient['name']).first()

            # ingredient = Quantity(
            #     value=ingredient['value'],
            #     recipe=recipe,
            #     ingredient=ingredient,
            # )

        return render_template(
            'main.html',
            title='Home',
            recipe_form=recipe_form,
        )

    return render_template(
        'main.html',
        title='Home',
        recipe_form=recipe_form,
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
