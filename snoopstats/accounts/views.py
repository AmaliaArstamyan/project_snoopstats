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
from accounts.login import LoginForm
from accounts.models import UserSettings


def user_logout(request):
    logout(request)  # This will log the user out
    # Optionally, clear user settings or reset them here
    if request.user.is_authenticated:
        user_settings = UserSettings.objects.get(user=request.user)
        user_settings.remember_password = False
        user_settings.save()
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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('register')  # Redirect back to register page
            
            # Create new user
            user = User.objects.create_user(username=username, email=email, password=password)
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
        form = LoginForm(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            remember_password = request.POST.get('remember_password')  # Get the checkbox value

            # Check if the input is an email or a username
            if '@' in username_or_email:  # It's an email
                user = authenticate(request, username=username_or_email, password=password)
            else:  # It's a username
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)

                # Check if the "Remember Password" checkbox is checked
                if remember_password == 'on':  # Checkbox is checked, remember the session
                    request.session.set_expiry(1209600)  # 2 weeks
                else:  # Checkbox is not checked, standard session expiration
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                return redirect('home')  # Redirect to home after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
