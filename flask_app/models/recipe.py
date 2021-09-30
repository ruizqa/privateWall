from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


# model the class after the friend table from our database
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.under_30min = data['under_30min']
        self.description = data['description']
        self.instructions=data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
# Now we use class methods to query our database
    @staticmethod
    def validate_recipe( recipe ):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Recipe name must be at least 3 characters long", "recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Recipe description must be at least 3 characters long", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Recipe instructions must be at least 3 characters long", "recipe")
            is_valid = False
        if len(recipe['made_on']) < 1 or len(recipe['under_30min'])<1:
            flash("All fields must be filled out", "recipe")
            is_valid = False
        return is_valid
    @classmethod
    def get_recipe_info(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        recipe = connectToMySQL('recipes_schema').query_db(query,data)
        return recipe[0]
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes ( name , under_30min , description , instructions, user_id, made_on, created_at, updated_at) VALUES ( %(name)s , %(under_30min)s , %(description)s ,%(instructions)s,%(user_id)s, %(made_on)s ,NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes_schema').query_db( query, data )
    @classmethod
    def update(cls, data ):
        query = "UPDATE recipes SET name = %(name)s , under_30min = %(under_30min)s,\
            description = %(description)s , instructions = %(instructions)s, user_id = %(user_id)s,\
                made_on = %(made_on)s, created_at = NOW(), updated_at = NOW() WHERE id = %(id)s"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes_schema').query_db( query, data )
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        recipes = connectToMySQL('recipes_schema').query_db(query)
        return recipes
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL('recipes_schema').query_db(query,data)