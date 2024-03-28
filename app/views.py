from django.shortcuts import redirect, render, get_object_or_404
from .models import Answer, Attempt, Choice, Question, Quiz
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

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if 'current_question_index' not in request.session:
        request.session['current_question_index'] = 0
        request.session['questions_order'] = list(quiz.questions.values_list('id', flat=True))
        random.shuffle(request.session['questions_order'])
        request.session.modified = True

    current_question_index = request.session['current_question_index']
    questions_order = request.session['questions_order']
    
    if current_question_index >= len(questions_order):
        return redirect('app:quiz_results', quiz_id=quiz_id)

    question_id = questions_order[current_question_index]
    question = Question.objects.get(id=question_id)
    
    return render(request, 'app/take_quiz.html', {'quiz': quiz, 'question': question})

@login_required
def submit_answer(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id, quiz=quiz)
    chosen_choice_id = int(request.POST.get('choice'))
    chosen_choice = get_object_or_404(Choice, id=chosen_choice_id, question=question)

    # Create or get the current attempt for the user
    attempt, _ = Attempt.objects.get_or_create(user=request.user, quiz=quiz)

    # Save the user's answer
    Answer.objects.create(attempt=attempt, question=question, chosen_choice=chosen_choice)

    # Increment the question index for the session
    request.session['current_question_index'] += 1
    request.session.modified = True

    return redirect('app:take_quiz', quiz_id=quiz.id)

@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    attempt = Attempt.objects.get(quiz=quiz, user=request.user)

    # Calculate score or retrieve it if you've saved it previously
    score = sum(1 for answer in attempt.answer_set.all() if answer.chosen_choice.is_correct)
    return render(request, 'app/quiz_results.html', {'quiz': quiz, 'attempt': attempt, 'score': score})

@login_required
def quiz_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest({"Invalid JSON"})
    
    quizzes = Quiz.objects.all()
    userQuizzes = serializers.serialize('json', quizzes)  # Retrieve all quiz objects from the database
    return render(request, 'app/index.html', {'quizzes': userQuizzes})


def submit_answer(request):
    if request.method == "POST":

                # Attempt to parse JSON from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        # Validate that all required fields are present
        required_fields = ['quizId', 'answer', 'questionId']
        if not all(field in data for field in required_fields):
            return HttpResponseBadRequest("Missing required fields")

        quizData = Quiz.objects.get(id=data['quizId'])
        if quizData and quizData.user == request.user:

            if len(quizData.unanswered) == 0:
                return JsonResponse({"success": False, "message": "No more questions to answer, please reload the page, the client may have fallen out of sync with the server."})

            currentQ = quizData.unanswered[0]

            if not int(currentQ['id']) == int(data['questionId']):
                return JsonResponse({"success": False, "message": "The client has fallen out of sync with the server, please reload the page."})

            if int(data['answer']) == int(currentQ['answer']):
                if quizData.correctlyAnswered == {}:
                    quizData.correctlyAnswered = [quizData.unanswered.pop(0)]
                else:
                    quizData.correctlyAnswered.append(quizData.unanswered.pop(0))
            else:
                questionData = quizData.unanswered.pop(0)
                if quizData.incorrectlyAnswered == {}:
                    quizData.incorrectlyAnswered = [{
                        "type": questionData['type'],
                        "question": questionData['question'],
                        "answer": questionData['answer'],
                        "userAnswer": data['answer'],
                        "id": questionData['id']
                    }]
                else:
                    quizData.incorrectlyAnswered.append(
                        {
                        "type": questionData['type'],
                        "question": questionData['question'],
                        "answer": questionData['answer'],
                        "userAnswer": data['answer'],
                        "id": questionData['id']
                        }
                    )
            quizData.save()
            return JsonResponse({"success": True, "correct": int(data['answer']) == int(currentQ['answer'])})
