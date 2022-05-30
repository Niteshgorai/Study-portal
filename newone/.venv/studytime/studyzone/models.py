# from termios import TIOCSWINSZ
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Registration(models.Model):
    fname=models.CharField(max_length=122)
    lname=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    password=models.CharField(max_length=10)
    address=models.TextField()
    city=models.CharField(max_length=122)
    zip=models.CharField(max_length=6)

    
class Notes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=130)
    description=models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="notes"
        verbose_name_plural="notes"

class Homework(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    title=models.CharField(max_length=130)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title
        

class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    title=models.CharField(max_length=100)
    is_finished=models.BooleanField(default=False)   

    def __str__(self):
        return self.title

class Newsletter(models.Model ):
    name = models.CharField(max_length=130,default="")
    email = models.EmailField(default="")
    # phone = models.CharField(max_length=12,default="")
    phone = PhoneNumberField()

    def __str__(self):
        return self.name