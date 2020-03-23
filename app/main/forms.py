from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, BooleanField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class IngredientForm(FlaskForm):
    value = StringField('Value')

    ingredient_name = StringField('Ingredient')

    unit_type = SelectField(u'Unit Type', choices=[
            ('teaspoon', 'teaspoon'),
            ('tablespoon', 'tablespoon'),
            ('fluid_ounce', 'fluid_ounce'),
            ('cup', 'cup'),
            ('pint', 'pint'),
            ('quart', 'quart'),
            ('gallon', 'gallon'),
            ('milliliter', 'milliliter'),
            ('liter', 'liter'),
            ('deciliter', 'deciliter'),
            ('pound', 'pound'),
            ('ounce', 'ounce'),
            ('milligram', 'milligram'),
            ('gram', 'gram'),
            ('kilogram', 'kilogram'),
            ('quantity', 'quantity'),
        ])


class RecipeForm(FlaskForm):
    name = StringField('Recipe name', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=30)


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
