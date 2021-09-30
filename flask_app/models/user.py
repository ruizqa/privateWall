# import the function that will return an instance of a connection
import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import message
from datetime import datetime as dt
from datetime import timedelta as td

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.messages = []
# Now we use class methods to query our database
    @staticmethod
    def validate_user( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['fname']) < 2:
            flash("First Name must be at least 2 characters long.", "register")
            is_valid = False
        if len(user['lname']) < 2:
            flash("Last Name must be at least 2 characters long.", "register")
            is_valid = False
        if user['pw'] != user['cpw']:
            flash("Your password does not match the password confirmed", "register")
            is_valid = False
        if len(user['pw']) < 8:
            flash("Your password must be at least 8 characters long", "register")
            is_valid = False
        return is_valid
    @staticmethod
    def validate_login( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "login")
            is_valid = False
        if len(user['pw']) < 8:
            flash("Please enter a password. Passwords are at least 8 characters long", "login")
            is_valid = False
        return is_valid
    @classmethod
    def login(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('private_wall').query_db(query,data)
        if len(result)<1:
            return False
        else:
            return cls(result[0])
    @classmethod
    def get_user_info(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('private_wall').query_db(query,data)
        if len(result)<1:
            return False
        else:
            return cls(result[0])
    @classmethod
    def get_all_users(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s ORDER BY first_name;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('private_wall').query_db(query,data)
        users=[]
        if len(result)<1:
            return False
        else:
            for i in range(len(result)):
                user = cls(result[i])
                users.append(user)
            return users
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('private_wall').query_db( query, data )

    def get_user_messages(self):
        data={'id': self.id}
        query= "SELECT messages.id, messages.created_at, messages.content, messages.sender_id, messages.receiver_id, TIMEDIFF(NOW(),messages.created_at) AS 'timediff' FROM users LEFT JOIN messages ON messages.receiver_id = users.id WHERE users.id = %(id)s AND messages.id IS NOT NULL ORDER BY users.first_name;"
        result = connectToMySQL('private_wall').query_db(query,data)
        if len(result)<1:
            return self
        else:
            for i in range(len(result)):
                message_u = message.Message(result[i])
                message_u.timediff = result[i]['timediff']
                if message_u.timediff < td(minutes=1):
                    message_u.timediff = f"{message_u.timediff.total_seconds()} seconds ago"
                elif message_u.timediff < td(hours=1):
                    s = message_u.timediff.total_seconds()
                    minutes, seconds = divmod(s, 60)
                    message_u.timediff = '{:02} minutes and {:02} seconds ago'.format(int(minutes), int(seconds))
                elif message_u.timediff < td(hours=24):
                    s = message_u.timediff.total_seconds()
                    hours, remainder = divmod(s, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    message_u.timediff = '{:02} hours and {:02} minutes ago'.format(int(hours), int(minutes))
                else:
                    s = message_u.timediff.total_seconds()
                    days, remainder = divmod(s,86400)
                    hours, remainder = divmod(remainder, 3600)
                    message_u.timediff = '{:02} days and {:02} hours ago'.format(int(days), int(hours))
                self.messages.append(message_u)
            return self