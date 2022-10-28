from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re

from flask_app.models.facilitie import Facilitie
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'ultrasounddb'
class Tech:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.facilities = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM techs;"
        results = connectToMySQL(DATABASE).query_db(query)
        techs = []
        for tech in results:
            techs.append( cls(tech) )
        return techs

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM techs WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        tech = Tech(result[0])
        return tech

    @classmethod
    def get_one_with_email(cls,data) -> object or bool:
        query = "SELECT * FROM techs WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        else:
            tech = Tech(result[0])
        return tech

    @classmethod
    def get_one_with_facilities(cls, data):
        query = "SELECT * FROM techs LEFT JOIN facilities ON techs.id = facilities.tech_id WHERE techs.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        tech = Tech(results[0])
        for result in results:
            facilitie_dict = {
                'id': result['facilities.id'],
                'name': result['name'],
                'description': result['description'],
                'instructions': result['instructions'],
                'date_made': result['date_made'],
                'under_30': result['under_30'],
                'tech_id': result['tech_id'],
                'created_at': result['facilities.created_at'],
                'updated_at': result['facilities.updated_at'],
            }
            tech.facilities.append(Facilitie(facilitie_dict))
        return tech

    @classmethod
    def save(cls, data):
        query = "INSERT INTO techs (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE techs SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_tech(tech:dict) -> bool:
        is_valid = True
        if len(tech['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 char", 'first_name')
        if len(tech['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 char", 'last_name')
        if not EMAIL_REGEX.match(tech['email']): 
            flash("Invalid email", 'email')
            is_valid = False
        if 'password' in tech:
            if tech['password'] != tech['password_confirmation']:
                flash("Mismatch, bro", 'password')
                is_valid = False
            if len(tech['password']) < 8:
                flash("password must be at least 8 char", 'password')
                is_valid = False
        return is_valid