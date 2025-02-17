from django.shortcuts import render
from django.contrib.auth.decorators import login_required




@login_required
def home(request):
    return render(request, 'home.html')


from django.shortcuts import render

# Landing page view
def landing_page(request):
    return render(request, 'landing_page/index.html')


# API
# views.py
from django.shortcuts import render
from .models import Post
from .services.google_search import search_google

def content_page(request):
    query = request.GET.get("q", "")
    results = search_google(query) if query else []

    # Get posts from the database (Google posts in this case)
    posts = Post.objects.filter(platform='google')  # Filter posts by platform (google)

    return render(request, "dashboard/content.html", {
        "google_results": results,
        "query": query,
        "posts": posts,
        "platforms": ['google', 'youtube', 'facebook'],  # Adjust if needed
    })
#________________About, Services, Contact Us
from django.shortcuts import render
from .models import WebsiteInfo

def index_page(request):
    about_info = WebsiteInfo.objects.filter(section='about').first()
    services_info = WebsiteInfo.objects.filter(section='services').first()
    contact_info = WebsiteInfo.objects.filter(section='contact').first()

    return render(request, "landing_page/index.html", {
        "about_info": about_info,
        "services_info": services_info,
        "contact_info": contact_info,
    })


# from django.shortcuts import render
# from .services.google_search import search_google

# import logging

# logger = logging.getLogger(__name__)

# def google_search_view(request):
#     query = request.GET.get("q", "")
#     logger.debug(f"Search Query: {query}")
#     results = search_google(query) if query else []
#     logger.debug(f"Search Results: {results}")
    
#     return render(request, "dashboard/content.html", {"results": results, "query": query})


