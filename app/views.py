from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Answer, Attempt, Choice, Question, Quiz
import random

def create_quiz(request):
    error_message = None
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if not title:
            error_message = "Title is required."
        else:
            quiz = Quiz(title=title, description=description, creator=request.user)
            quiz.save()
            return redirect('add_questions', quiz_id=quiz.id)
    return render(request, 'quizzes/create_quiz.html', {'error_message': error_message})

def add_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        # Assume you have fields for choices and correct answer
        question = Question(quiz=quiz, text=text)
        question.save()
        # Redirect or render as needed, possibly to add more questions or to the quiz detail page
        return redirect('add_questions', quiz_id=quiz.id)
    return render(request, 'quizzes/add_questions.html', {'quiz': quiz})

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
        return redirect('quiz_results', quiz_id=quiz_id)

    question_id = questions_order[current_question_index]
    question = Question.objects.get(id=question_id)
    
    return render(request, 'app/take_question.html', {'quiz': quiz, 'question': question})

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

    return redirect('take_quiz', quiz_id=quiz.id)

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    attempt = Attempt.objects.get(quiz=quiz, user=request.user)

    # Calculate score or retrieve it if you've saved it previously
    score = sum(1 for answer in attempt.answer_set.all() if answer.chosen_choice.is_correct)
    return render(request, 'app/quiz_results.html', {'quiz': quiz, 'attempt': attempt, 'score': score})

def quiz_view(request):
    quizzes = Quiz.objects.all()  # Retrieve all quiz objects from the database
    return render(request, 'app/index.html', {'quizzes': quizzes})