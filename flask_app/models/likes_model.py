from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Like:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.show_id = data['show_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_num_of_likes_for_each_show(cls, data):
        query = """
                SELECT COUNT(id)
                FROM likes
                WHERE show_id = %(show_id)s
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        print(results[0]['COUNT(id)'])
        #the number of likes each show has when the query is ran
        return results[0]['COUNT(id)']
    
    @classmethod
    def create_a_like(cls,data):
        query = """
                INSERT INTO likes (user_id, show_id, created_at, updated_at)
                VALUES (%(user_id)s, %(show_id)s, NOW(), NOW())
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all_likes(cls, data):
        query = """
                SELECT *
                FROM likes
                WHERE user_id = %(user_id)s;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        all_user_likes = []
        if results:
            for row in results:
                users_likes = cls(row)
                all_user_likes.append(users_likes)
            
        return all_user_likes