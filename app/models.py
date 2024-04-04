from django.db import models
from django.contrib.auth.models import User
import uuid

class Quiz(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='quizzes')
    questionData = models.JSONField(default=dict, blank=True, null=True)
    def __str__(self):
        return self.id

class Attempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    completed = models.BooleanField(default=False)
    answeredQuestions = models.JSONField(default=list, blank=True)
    unansweredQuestions = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Attempt {self.id} by {self.user.username}"