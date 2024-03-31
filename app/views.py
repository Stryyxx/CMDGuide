from django.shortcuts import redirect, render, get_object_or_404
from .models import Quiz, Attempt
import random
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.http import JsonResponse
from django.core import serializers



@login_required
def create_quiz(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest({"Invalid JSON"})
        
        # Validate that all required fields are present
        required_fields = ['quizData']
        if not all(field in data for field in required_fields):
            return HttpResponseBadRequest("Missing required fields")
        
        quiz_data = data['quizData']
        questions = quiz_data['questions']
        quiz = Quiz(user=request.user, unanswered=questions);
        return JsonResponse({"success": True, "quizId": quiz.id})
    else:
        return render(request, 'app/create_quiz.html')

def index(request):
    return render(request, 'app/index.html')
