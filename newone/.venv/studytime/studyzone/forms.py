from logging import PlaceHolder
from tkinter import Widget
from turtle import title
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
# from django.forms import ModelForm



class RegistrationForm(forms.ModelForm):
    class Meta:
        model=Registration
        fields=['fname','lname','email','password','address','zip']

class NotesForm(forms.ModelForm):
    class Meta:
        model= Notes
        fields= ['title','description']


class DateInput(forms.DateInput):
    input_type='date'

class HomeworkForm(forms.ModelForm):
    # my_date_field = forms.DateField(
    #     widget=forms.DateInput(format=('%d-%m-%Y'), 
    #                            attrs={'due':'myDateClass', 
    #                            'placeholder':'Select a date'}))
    class Meta:
        model=Homework
        Widget={'due':DateInput()}
        fields=['subject','title','description','due','is_finished',]
        # widgets = {
        #     'due': forms.DateInput(
        #         format=('%d/%m/%Y'),
        #         attrs={'class': 'form-control', 
        #                'placeholder': 'Select a date',
        #                'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
        #               }),
        # }

class DashboardFom(forms.Form):
    text= forms.CharField(max_length=100, label="Enter your Search :")


class TodoForm(forms.ModelForm):
    class Meta:
        model= Todo
        fields= ['title', 'is_finished']

class ConversionForm(forms.Form):
    CHOICES=[('length','Length'),('mass','Mass')]
    measurement=forms.ChoiceField(choices =CHOICES,widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES=[('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','Placeholder':"Enter the Number"}
    ))
    measure1=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )

    measure2=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )

class ConversionMassForm(forms.Form):
    CHOICES=[('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','Placeholder':"Enter the Number"}
    ))
    measure1=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )

    measure2=forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']
