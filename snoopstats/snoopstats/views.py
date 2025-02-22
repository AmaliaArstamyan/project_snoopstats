from django.shortcuts import render
from django.contrib.auth.decorators import login_required




@login_required
def home(request):
    return render(request, 'home.html')


from django.shortcuts import render

# Landing page view
def landing_page(request):
    return render(request, 'landing_page/index.html')


# _______________________________________________API
# views.py
from django.shortcuts import render
from snoopstats.services.google_search import search_google
from snoopstats.services.youtube_scraper import search_youtube
from snoopstats.services.facebook_search import search_facebook
from snoopstats.models import Post

def content_page(request):


    posts = Post.objects.all()  # Load all posts
    active_platform = request.GET.get('platform', 'google') 


     

    
    platforms = {
        "google": posts.filter(platform="google"),
        "youtube": posts.filter(platform="youtube"),
        "facebook": posts.filter(platform="facebook"),
    }

    return render(request, "dashboard/content.html", {"platforms": platforms, "active_platform": active_platform})






#________________________________________________________________________________________________________

#________________About, Services, Contact Us
from django.shortcuts import render
from .models import WebsiteInfo

def index_page(request):
    about_info = WebsiteInfo.objects.filter(section='about').first()
    services_info = WebsiteInfo.objects.filter(section='services').first()
    contact_info = WebsiteInfo.objects.filter(section='contact').first()

    context = {
        "about_info": about_info,
        "services_info": services_info,
        "contact_info": contact_info,
    }
    
    return render(request, "landing_page/index.html", context)

# Statystics view
def statistics(request):
    return render(request, 'dashboard/statistics.html')


