from django.db import models
from datetime import date
import re

class UserManager(models.Manager):
    def validate_user(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be at least 2 character"
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 character"

        if not re.match('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', postData['email']):
            errors['email'] = 'Email address is an invalid format'
        
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Password and confirmation password must match'

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def validate_trip(self, postData):
        errors = {}
        
        if len(postData['destination']) < 3:
            errors['destination'] = 'A trip destination must consist of at least three characters.'
        
        today = str(date.today())
        if postData['start_date'] < today:
            errors['start_date'] = "You can't take a trip in the past."

        if postData['start_date'] > postData['end_date']:
            errors['end_date'] = 'Start date must be before end date'

        if len(postData['plan']) < 4:
            errors['plan'] = 'A plan must be provided!'

        return errors

class Trip(models.Model):
    travelers = models.ManyToManyField(User, related_name="trips_joined")
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_by = models.ForeignKey(User, related_name="trips_created", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()


