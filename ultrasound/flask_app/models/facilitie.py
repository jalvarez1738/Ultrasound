from flask_app.config.mysqlconnection import connectToMySQL
from operator import is_
from flask_app import flash
from pprint import pprint

from flask_app.models.tech import Tech

DATABASE = 'ultrasounddb'

class Facilitie:
    def __init__( self , data ):
        self.id = data['id']
        self.namd = data['name']
        self.address = data['address']
        self.email = data['email']
        self.password = data['password']
        self.tech_id = data['tech_id']
        if 'first_name'in data:
            self.first_name = data['first_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT facilities.*, first_name FROM facilities JOIN techs ON techs.id = facilities.tech_id WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query)
        facilities = []
        for facilitie in results:
            facilities.append( cls(facilitie) )
        return facilities

    @classmethod
    def get_all_with_tech(cls):
        query = "SELECT * FROM facilities JOIN techs ON facilities.tech_id = techs.id ;"
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        facilities = []
        for facilitie in results:
            facilities.append( cls(facilitie) )
        return facilities

    @classmethod
    def get_one(cls, data):
        query = "SELECT facilities.*, first_name FROM facilities JOIN techs ON techs.id = facilities.tech_id WHERE facilities.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        facilitie = Facilitie(result[0])
        return facilitie

    @classmethod
    def save(cls, data):
        query = "INSERT INTO facilities (name, address, email, password, tech_id) VALUES (%(name)s, %(address)s, %(email)s, %(password)s, %(tech_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM facilities WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_facilitie(facilitie:dict) -> bool:
        is_valid = True
        if len(facilitie['name']) < 3:
            flash('Name must be at least 3 char')
            is_valid = False
        if len(facilitie['address']) < 3:
            flash('Address must be at least 3 char')
            is_valid = False
        if len(facilitie['password']) < 3:
            flash('Password must be at least 3 char')
            is_valid = False
        return is_valid

    @classmethod
    def update(cls, data):
        query = "UPDATE facilities SET name = %(name)s, address = %(address)s, email = %(email)s, password = %(password)s, tech_id = %(tech_id)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)