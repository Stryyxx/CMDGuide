from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quizzes/create/', views.create_quiz, name='create_quiz'),
]