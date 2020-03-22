import enum

from datetime import datetime
from hashlib import md5
from app import db, login
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.relationship('Quantity', backref='recipe', lazy=True, passive_deletes=True)

    def __repr__(self):
        return '<Recipe {}>'.format(self.body)


class UnitTypesEnum(enum.Enum):
    # Volume
    teaspoon = 'teaspoon'
    tablespoon = 'tablespoon'
    fluid_ounce = 'fluid once'
    cup = 'cup'
    pint = 'pint'
    quart = 'quart'
    gallon = 'gallon'
    milliliter = 'milliliter'
    liter = 'liter'
    deciliter = 'deciliter'

    # Mass and Weight
    pound = 'pound'
    ounce = 'ounce'
    milligram = 'milligram'
    gram = 'gram'
    kilogram = 'kilogram'

    # Quantity
    quantity = 'quantity'


class Quantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False, default=0)
    ingredient_name = db.Column(db.String(140))
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipe.id', ondelete='CASCADE'),
        nullable=False)
    unit_type = db.Column(
        db.Enum(UnitTypesEnum),
        nullable=True
    )


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    food_group = db.Column(db.String(180), nullable=True)
    food_subgroup = db.Column(db.String(180), nullable=True)
    food_type = db.Column(db.String(180), nullable=True)
    type_quantity = db.Column(db.Boolean, default=False)
    type_volume = db.Column(db.Boolean, default=False)
    type_weight = db.Column(db.Boolean, default=False)
