from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quiz_list/", views.quiz_list, name="quiz_list"),
    path("create_quiz", views.create_quiz, name="create_quiz")
]