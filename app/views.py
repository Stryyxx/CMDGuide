from django.shortcuts import redirect, render, get_object_or_404
from .models import Quiz, Attempt
import random
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.http import JsonResponse
from django.core import serializers

# View function for creating a quiz
@login_required
def create_quiz(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # Return error response if JSON decoding fails
            return HttpResponseBadRequest({"Invalid JSON"})
        
        # Validate that all required fields are present
        required_fields = ['quizData']
        if not all(field in data for field in required_fields):
            # Return error response if required fields are missing
            return HttpResponseBadRequest("Missing required fields")
        
        quiz_data = data['quizData']
        questions = quiz_data['questions']
        # Create a new Quiz object with the user and unanswered questions
        quiz = Quiz(user=request.user, unanswered=questions)
        # Return success response with quiz ID
        return JsonResponse({"success": True, "quizId": quiz.id})
    else:
        # Render the create quiz template for GET requests
        return render(request, 'app/create_quiz.html')

# View function for the index page
def index(request):
    # Render the index page
    render(request, 'app/index.html')
