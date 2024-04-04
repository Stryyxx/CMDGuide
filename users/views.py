from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# View function for user login
def login_view(request):
    if request.method == "POST":
        # Retrieve username and password from form data
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If authentication succeeds, log in the user and redirect to home page
            login(request, user)
            return redirect('/')
        else:
            # If authentication fails, render login page with error message
            return render(request, "users/login.html", {
                'message': {
                    "text": "Credentials combination does not match our records.",
                    "type": "Error",
                    "class": "errorBox"
                }
            })
    # Render login page for GET requests
    return render(request, "users/login.html")

# View function for user logout
def logout_view(request):
    # Log out the user and render login page with success message
    logout(request)
    return render(request, "users/login.html", {
        "message": {
            "text": "Successfully Logged Out",
            "type": "Success",
            "class": "successBox"
        }
    })

# View function for user signup
def signup_view(request):
    if request.method == "POST":
        # Retrieve username, password, and confirmation password from form data
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "users/signup.html", {
                "message": {
                    "text": "Username already exists. Please choose a different username.",
                    "type": "Error",
                    "class": "errorBox"
                }
            })

        # Check if password and confirmation password match
        if password != confirmPassword:
            return render(request, "users/signup.html", {
                "message": {
                    "text": "Passwords do not match.",
                    "type": "Error",
                    "class": "errorBox"
                }
            })

        try:
            # Create a new user
            user = User.objects.create_user(username=username, email=None, password=password)
            user.save()

            # Log in the new user and redirect to home page
            login(request, user)
            return redirect('/')
        except Exception as e:
            # Render signup page with error message if an unexpected error occurs
            print("Unable to create user:", e)
            return render(request, "users/signup.html", {
                "message": {
                    "text": "An unexpected error occurred. Please try again later.",
                    "type": "Error",
                    "class": "errorBox"
                }
            })

    # Render signup page for GET requests
    return render(request, "users/signup.html")
