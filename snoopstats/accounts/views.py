from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from accounts.forms import RegisterForm
from accounts.login import LoginForm  # Updated import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def user_logout(request):
    logout(request)  # This will log the user out
    return redirect('login')  # Redirect to the login page

@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to home page
            else:
                messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # Use email as username
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if the user is already logged in

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                # If user is None, authentication failed
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})