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
from services.google_search import search_google
from services.youtube_scraper import search_youtube
from services.facebook_search import search_facebook
from snoopstats.models import Post

def content_page(request):
    query = request.GET.get('q', '')

    google_results, youtube_results, facebook_results = [], [], []

    if query:
        google_results = search_google(query)
        youtube_results = search_youtube(query)
        facebook_results = search_facebook(query)

    context = {
        "query": query,
        "google_results": google_results,
        "youtube_results": youtube_results,
        "facebook_results": facebook_results,
        "platforms": ["google", "youtube", "facebook"],
    }

    return render(request, "your_template.html", context)






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


