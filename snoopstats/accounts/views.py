from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from accounts.login import LoginForm  # Updated import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
# views.py
from .forms import RegisterForm



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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            # Create the user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('register')  # Redirect back to register page
            
            # Create new user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            messages.success(request, "Your account has been created successfully! Please log in.")
            return redirect('login')  # Redirect to login page after successful registration
        
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user using the provided credentials
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # If the user is authenticated, log them in
            login(request, user)
            return HttpResponseRedirect('/')  # Redirect to home or any other page
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid email or password")
            return redirect('login')  # Redirect back to the login page

    return render(request, 'login.html')  # Render the login page if GET request