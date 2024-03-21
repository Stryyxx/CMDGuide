from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view, name='quiz_list'),
    path('quizzes/create/', views.create_quiz, name='create_quiz'),
    path('quizzes/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quizzes/<int:quiz_id>/submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('quizzes/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
]