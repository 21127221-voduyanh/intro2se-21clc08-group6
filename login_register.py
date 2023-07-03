import pyodbc
import socket

SERVER_NAME = socket.gethostname()+'\SQLEXPRESS'

connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER_NAME+';Database=CNPM; UID=john; PWD=123456;')
cur = connection.cursor()

def register_finder():
    type = 'f'
    check = 0 
    while check == 0:
        name = input("Username:")
        if (name.isalnum()  and name.islower() and len(name) < 16):
            check = 1
        else:
            print("Username too long or contain special characters or only contain digits")
        cur.execute("select USERNAME from ACCOUNT where USERNAME = ?",name)
        user=cur.fetchone()
        if (user is None):
            check = 1
        else:
            print("User name existed, please pick another one")
            check = 0
    check2 = 0 
    while check2 == 0:
        password = input("Password:")
        if len(password) >= 8 and len(password) <= 32:
            check2 = 1
    confpassword = input("Confirm your password:")
    while password != confpassword:
        confpassword = input("Confirm your password:")
    cur.execute("insert ACCOUNT values (?,?,?)",name,password,type)
    full_name = input("Full name:")
    address = input("Address:")
    city = input("City:")
    intro = input("Introduction:")

def register_employer():
    type = 'e'
    check = 0 
    while check == 0:
        name = input("Username:")
        if (name.isalnum()  and name.islower() and len(name) < 16):
            check = 1
        else:
            print("Username too long or contain special characters or only contain digits")
        cur.execute("select USERNAME from ACCOUNT where USERNAME = ?",name)
        user=cur.fetchone()
        if (user is None):
            check = 1
        else:
            print("User name existed, please pick another one")
            check = 0
    check2 = 0 
    while check2 == 0:
        password = input("Password:")
        if len(password) >= 8 and len(password) <= 32:
            check2 = 1
    confpassword = input("Confirm your password:")
    while password != confpassword:
        confpassword = input("Confirm your password:")
    cur.execute("insert ACCOUNT values (?,?,?)",name,password,type)
    comp_name = input("Company name:")
    address = input("Address:")
    city = input("City:")
    intro = input("Introduction:")

def login():
    check = 0
    while check == 0:
        name = input("Username:")
        cur.execute("select USERNAME from ACCOUNT where USERNAME = ?",name)
        user = cur.fetchone()
        if (user is None):
            print("Username is not existed, please try again")
        else:
            check = 1
    check2 = 0
    while check2 == 0:
        password = input("Password:")
        cur.execute("select PASS_WORD from ACCOUNT where USERNAME = ?", name)
        pass_word = cur.fetchone()
        if password == pass_word:
            check2 = 1
            print("Login successfully")
        else:
            print("Password does not match, please try again")
#register_finder()
#register_employer()
login()


'''
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    introduction = models.TextField()


from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'password1', 'password2', 'address', 'city', 'introduction')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'address', 'city', 'introduction')
'''
