from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')


from django.shortcuts import render

# Landing page view
def landing_page(request):
    return render(request, 'landing_page/index.html')