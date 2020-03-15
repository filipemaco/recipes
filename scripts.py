import json
from app.models import Ingredient
from app import db


def add_ingredients():
    with open('/Users/filipe/recipes/foods.json') as f:
        ingredients = json.load(f)

    for ingredient in ingredients:
        name = ingredient['name']
        if not name:
            continue

        food_type = ingredient['food_type'] if ingredient['food_type'] else None
        food_group = ingredient['food_group'] if ingredient['food_group'] else None

        ingredient = Ingredient(
            name=name,
            food_group=food_group,
            food_type=food_type,
            type_quantity=True,
            type_volume=False,
            type_weight=False
        )

        db.session.add(ingredient)
        db.session.commit()
