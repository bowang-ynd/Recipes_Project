from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Recipe:

    # class constructor
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']

        # additionally add a owner_name for each recipe
        self.owner_name = ""
    
    # An instance method to set each instance's owner_name
    def set_owener_name(self, name):
        self.owner_name = name

    #? ==================== CREATE ====================
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes (name, description, instruction, date_made, under_30, owner_id)
            VALUES (%(name)s, %(description)s, %(instruction)s, %(date_made)s, %(under_30)s, %(owner_id)s);
        """

        connectToMySQL(DATABASE).query_db(query, data)
    
    #? ==================== READ ====================
    @classmethod
    def get_one_recipe(cls, data):
        query = """
            SELECT * FROM recipes 
            JOIN users ON users.id = recipes.owner_id
            WHERE recipes.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        # if no recipes found, return false
        if (not results) or (len(results) <= 0):
            return False
        
        # else instantiate and return the found recipe 
        found_recipe = cls(results[0])
        found_recipe.set_owener_name(results[0]['first_name'])
        return found_recipe
    
    @classmethod # get all existing recipes
    def get_all(cls):
        query = """
            SELECT * FROM recipes
            JOIN users ON users.id = recipes.owner_id;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        # if no recipes found, return false
        if (not results) or (len(results) <= 0):
            return False
        # else instantiate and return all found recipes 
        found_recipes = []

        for result in results:
            recipe = cls(result)
            recipe.set_owener_name(result['first_name'])
            found_recipes.append(recipe)
        return found_recipes
    
    #? ==================== UPDATE ====================
    @classmethod
    def edit_recipe_with_id(cls, data):
        query = """
            UPDATE recipes
            SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, under_30 = %(under_30)s, date_made = %(date_made)s
            WHERE recipes.id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)
    
    #? ==================== DELETE ====================
    @classmethod
    def delete_recipe_with_id(cls, data):
        query = """
            DELETE FROM recipes WHERE recipes.id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

    #? ==================== VALIDATION ====================
    @staticmethod
    def validate_recipe(data):
        is_valid = True

        #! ========== Checking NAME ==========
        # Name should not be void
        if len(data['name']) == 0:
            flash("Name should not be blank!", "recipe")
            is_valid = False
        # Name should be at least 3 chars
        elif len(data['name']) < 3:
            flash("Name should be at least 3 characters!", "recipe")
            is_valid = False

        #! ========== Checking DESCRIPTION ==========
        # Name should not be void
        if len(data['description']) == 0:
            flash("Description should not be blank!", "recipe")
            is_valid = False
        # Name should be at least 3 chars
        elif len(data['description']) < 3:
            flash("Description should be at least 3 characters!", "recipe")
            is_valid = False

        #! ========== Checking INSTRUCTION ==========
        # Name should not be void
        if len(data['instruction']) == 0:
            flash("Instruction should not be blank!", "recipe")
            is_valid = False
        # Name should be at least 3 chars
        elif len(data['instruction']) < 3:
            flash("Instruction should be at least 3 characters!", "recipe")
            is_valid = False

        #! ========== Checking DATE ==========
        # DATE should not be empty
        if len(data['date_made']) == 0:
            flash("Please select Cooked/Made date", "recipe")
            is_valid = False
        
        return is_valid