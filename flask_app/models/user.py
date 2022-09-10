#In the models folder, we need to create a folder and name in the singlar verson of the file in the controllers folder
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# create a regular expression object that we'll use later (validation)   
import re	# the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# This regex will enforce these rules:
# At least one upper case English letter, (?=.*[A-Z])
# At least one lower case English letter, (?=.*[a-z])
# At least one digit, (?=.*[0-9])
PASSWORD_REGEX =re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z\d]+$")
# At least one special character, (?=.*[#?!@$%^&*-])
# Minimum eight in length .{8,} (with the anchors)
# PASSWORD_REGEX =re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[#?!@$%^&*-]).{8,}$')


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#-- -------------------------Registration (Create User Step 3 of 3) --------------------------
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL("login_and_reg_assignment").query_db(query, data)
        print(results)
        return results


# --------------------Login (Comparing Upon Login step 3 of 3)--------------------------------------
    @classmethod
    def get_by_email (cls, data): 
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('login_and_reg_assignment').query_db(query, data) 
        print(results)
        # this if statement is for the validating if the email already exist in the database
        if results == (): #when we pass in an email not inside the database it returns an empty tuple ()
            return False
        # otherwise we are creating an users instance from the single list of one dictionary that we get
        return (cls(results[0])) #we are returning the users instance to the controller route



# ********The following methods are for inside of our app. The login and Registration is the front door*********
# ------------------------Read one (step 3 of 3)-------------------------------
    @classmethod
    def get_by_id (cls, data): #data is being passed into the class method from the route in the controllers file
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL("login_and_reg_assignment").query_db(query, data) #data needs to be added to the query_db because we are passing that information from the data dictionary created in the controllers file
        print(results)
        # we are creating an users instance from the single list of one dictionary that we get
        return (cls(results[0])) #we are returning the users instance to the controller route



# --------------------validation (step 3 of 3)-----------------------------------
    @staticmethod
    def validate_create(user): #user is the form information that we are passing in
        is_valid = True
        if len(user["first_name"]) <2:
            flash("First name is too short!", "create_user") #"create_user" is the validation catagory filter
            is_valid = False
        if len(user["last_name"]) <2:
            flash("last name is too short!", "create_user")
            is_valid = False
        if len(user["email"]) <6:
            flash("Email is too short!", "create_user")
            is_valid = False
        # The EMAIL_REGEX object has a method called .match() that will return None if no match can be found. If the argument matches the regular expression, a match object instance is returned.
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address format!", "create_user")
            is_valid = False
        # The PASSWORD_REGEX object has a method called .match() that will return None if no match can be found. If the argument matches the regular expression, a match object instance is returned.
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Invalid password format! Need 1 uppercase letter and 1 number", "create_user")
            is_valid = False
        if len(user["password"]) <8:
            flash("Password is too short!", "create_user")
            is_valid = False
        #if the value of password does not equal to the password conf
        if user["password"] != user["password_conf"]: 
            flash("Password do not match!", "create_user")
            is_valid = False
        # If the email is already in database (this requires a query to check if the email is in the database)
        # Becuase the classmethod requires us to pass in a data dictionary, we need to create one for the entered email
        data = {
            "email" : user["email"]
        }
        user_in_db = User.get_by_email(data) 
        # the code above will either return an empty tuple() or it will return a user instance becuase the email wasnt there and it was able to create an instance
        if user_in_db:
            flash("Email already taken.", "create_user")
            is_valid = False
        return is_valid
