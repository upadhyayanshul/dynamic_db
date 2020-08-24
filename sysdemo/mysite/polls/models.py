## UNICODE LITERALS ##
from __future__ import unicode_literals

## DEFINE THE USER ,PROFILE AND PRODUCT MODELS HERE ##
from django.db import models

## INBUILT AUTH MODEL OF DJANGO (EXTEND WITH THE PROFILE PROPERTY)
from django.contrib.auth.models import User


## DEFINE THE PROFILE MODEL WITH ONE RELATION WITH DJANGO AUTH MODEL (FOR ADVANTAGES)
class Profile(models.Model):
    
    # DJANGO AUTH MODEL RELATION DEFINATION WITH ONE TO ONE RELATION
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name ="user")
    
    # DEFINE OTHER FIELDS LIKE email,signup_confirmation,address,age,database_access(multiple array)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    address = models.CharField(blank=False, max_length=150)
    age = models.IntegerField()
    database_access = models.CharField(max_length=2000)
    
    # DEFINE THE MODEL TIME STAMP (WE CAN IMPORT FROM A BASE CLASS AS WELL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # DEFINE THE UNICODE PROPERTY TO SEE FIELDS IN DJANGO ADMIN
    def __unicode__(self):
        return self.user.username


## DEFINE THE PRODUCT MODEL WITH ForeignKey RELATION WITH DJANGO AUTH USER MODEL (FOR ADVANTAGES)
class Product(models.Model):
    
    # DEFINE THE CURRENCY CHOICES
    currencies = [
    ('$', "US Dollars ($)"), 
    ]

    # DEFINE ONE OF THE DATABASE CHOICE
    CHOICES = (('database_1', 'database_1'),
               ('database_2', 'database_2'),
               ('database_3', 'database_3'),
               ('database_4', 'database_4'),
               ('database_5', 'database_5'),
               ('default', 'dafault'),
               )
    # DEFIEN OTHER PROPERTIES FRO THE PRODUCT MODEL 
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=120)
    currency = models.CharField(max_length=5, choices=currencies, default="$",blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    active = models.BooleanField(default=True)
    description = models.TextField(blank = False)
    product_database = models.CharField(choices=CHOICES,max_length=40)
    user_id = models.IntegerField()

    # PRODUCT MODEL TIMESTAMP HERE 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # DEFINE THE UNICODE PROPERTY TO SEE FIELDS IN DJANGO ADMIN
    def __unicode__(self):
        return self.name