from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

passwd_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # name validation
        if len(postData['first_name']) < 2 or not name_regex.match(postData['first_name']):
            errors["first_name"] = "Please enter a valid first name"
        if len(postData['last_name']) < 2 or not name_regex.match(postData['last_name']):
            errors["last_name"] = "Please enter a valid last name"
        # email validation
        if len(postData['email1']) == 0 or not email_regex.match(postData['email1']):
            errors["email"] = "Please enter a valid email address"
        # email confirmation
        if postData['email1'] != postData['email2']:
            errors["email"] = "Email addresses did not match. Please enter emails again."
        # user validation
        valid_email = User.objects.filter(email = postData['email1'])
        if len(valid_email):
            errors["email"] = "There is already an account created with this email address. Please either login in using this address, or create an account with a different email address."
        # password validation
        if len(postData['passwd1']) < 9:
            errors['passwd1'] = "Password must be greater than 8 characters long"
        else:
            if not passwd_regex.match(postData['passwd1']):
                errors["passwd1"] = "Password must contain at least one digit, one lowercase letter, and one uppercase letter."
            else:
                if postData['passwd1'] != postData['passwd2']:
                    errors["email"] = "Password did not match. Please try again."
        # return error messages
        return errors

    def login_validator(self, postData):
        context = {'errors' : {}, 'user': {}}
        errors = {}
        # validate email
        if len(postData['email'])  == 0 or not email_regex.match(postData['email']):
            errors["email"] = "Please enter a valid email address"
        # validate password
        if len(postData['passwd'])  == 0 or not passwd_regex.match(postData['passwd']):
            errors["password"] = "Invalid password, please try again."
            context['errors'] = errors
            return context
        else:
            # user validation
            try:
                user = User.objects.get(email = postData['email'])
            except:
                errors["email"] = "Email address not registered, try again."
                context['errors'] = errors
                return context
            if not bcrypt.checkpw(postData['passwd'].encode(), user.password.encode()):
                errors["email"] = "Authentication failed, try again."
                context['errors'] = errors
                return context
            else:
                context['user'] = user.first_name
        # return error messages
        return context

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return "<User object {} {} {} {}".format(self.first_name, self.last_name, self.email, self.password)
