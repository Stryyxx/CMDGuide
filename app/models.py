from django.db import models
from django.contrib.auth.models import User
import uuid

class Quiz(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unanswered = models.JSONField(default=dict)
    incorrectlyAnswered = models.JSONField(default=dict, blank=True, null=True)
    correctlyAnswered = models.JSONField(default=dict, blank=True, null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='quizzes')
    def __str__(self):
        return (f"Quiz ID: {self.id}, User: {self.user.username}, "
                f"Unanswered: {self.unanswered}, Incorrectly Answered: {self.incorrectlyAnswered}, "
                f"Correctly Answered: {self.correctlyAnswered}, Completed: {self.completed},")

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title}'

class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.attempt} - {self.question.text} - {self.chosen_choice.text}'

