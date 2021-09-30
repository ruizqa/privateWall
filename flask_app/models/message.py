from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
# model the class after the friend table from our database
class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.sender = user.User.get_user_info({'id': data['sender_id']})
        self.timediff = None
# Now we use class methods to query our database
    @staticmethod
    def validate_message( message ):
        is_valid = True
        # test whether a field matches the pattern
        if len(message['content']) < 5:
            flash("The content of the message should be at least 5 characters long", "message")
            is_valid = False
        return is_valid
    @classmethod
    def get_message(cls,data):
        query= "SELECT * FROM messages WHERE id = %(id)s ;"
        result = connectToMySQL('private_wall').query_db(query,data)
        if len(result)<1:
            return False
        else:
            return cls(result[0])
    @classmethod
    def send(cls, data ):
        query = "INSERT INTO messages ( created_at , content , sender_id , receiver_id) VALUES ( NOW(), %(content)s , %(sender_id)s , %(receiver_id)s);"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('private_wall').query_db( query, data )
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('private_wall').query_db( query, data )