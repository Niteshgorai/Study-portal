from django.contrib import admin
from django.contrib.auth import views
from django.urls import path
from studyzone import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("", views.index, name='home'),
    # path("registration", views.registration, name='registration'),
    
    # path("login", views.login, name='login'),
    # path("login", auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    
    path("wikipedia", views.wikipedia, name='wikipedia'),
    
    path("dictionary", views.dictionary, name='dictionary'),
    path("blog", views.blog, name='blog'),
    path("about", views.about, name='about'),
    path("conversion", views.conversion, name='conversion'),
    path("notes", views.notes, name='notes'),
    path("delete_note/<int:pk>", views.delete_note, name='delete-note'),
    path("notesview/<int:pk>", views.NotesDetailView.as_view(), name='notesview'),

    path("homework", views.homework, name='homework'),
    path("updatehomework/<int:pk>", views.updatehomework, name='updatehomework'),
    path("deletehomework/<int:pk>", views.deletehomework, name='deletehomework'),
    path("youtube", views.youtube, name='youtube'),
    path("todo", views.todo, name='todo'),
    path("updatetodo/<int:pk>", views.updatetodo, name='updatetodo'),
    path("deletetodo/<int:pk>", views.deletetodo, name='deletetodo'),
    path("books", views.books, name='books'),
    path("newsletter", views.newsletter, name='newsletter'),


    # path("testing", views.testing, name='testing'),
]