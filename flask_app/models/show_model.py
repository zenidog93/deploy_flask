from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import user_model

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def create_show(cls, data):
        query = """
                INSERT INTO shows (title, network, release_date, description, created_at, updated_at, user_id)
                VAlUES ( %(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), NOW(), %(user_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update_show(cls, data):
        query = """
                UPDATE shows
                SET 
                    title = %(title)s, 
                    network = %(network)s,
                    release_date = %(release_date)s, 
                    description = %(description)s, 
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete_show(cls, data):
        query = """
                DELETE 
                FROM shows 
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update_show(cls, data):
        query = """
                UPDATE shows
                SET 
                    title = %(title)s, 
                    network = %(network)s,
                    release_date = %(release_date)s, 
                    description = %(description)s 
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete_show(cls, data):
        query = """
                DELETE 
                FROM shows 
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one_show_for_edit(cls,data):
        query = """
                SELECT *
                FROM shows
                JOIN users
                ON users.id = shows.user_id
                WHERE shows.id = %(id)s; 
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results: 
            this_show = cls(results[0])
            row = results[0]
            user_data = {
                    **row,
                    'id' : row['user_id'],
                    'created_at' : row['created_at'],
                    'updated_at' : row["updated_at"]
            }
            this_user = user_model.User(user_data)
            this_show.creator = this_user
            return this_show
        return False
            
    @classmethod
    def get_all_shows(cls):
        query  = """
                SELECT *
                FROM shows
                JOIN users
                ON users.id = shows.user_id
                """
        results = connectToMySQL(DATABASE).query_db(query)
        
        all_shows = []
        
        if results : 
            for row in results: 
                this_show = cls(row)
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                
                this_user =user_model.User(user_data)
                this_show.creator = this_user
                all_shows.append(this_show)
        return all_shows
    
    
    @staticmethod
    def validate_show(recipe_submission):
        is_valid = True
        if len(recipe_submission['title']) < 3:
            is_valid = False
            flash("Title has to be longer than 3 characters")
        
        if len(recipe_submission['network']) < 1:
            is_valid = False
            flash("You must enter some network :) ") 
        
        if len(recipe_submission['release_date']) < 1:
            is_valid = False
            flash("You must enter a release_date")
            
        if len(recipe_submission['description']) < 1: 
            is_valid = False
            flash("Must enter some description")   
        return is_valid