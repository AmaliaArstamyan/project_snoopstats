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
from .services.google_search import search_google

def content_page(request):
    query = request.GET.get("q", "")
    # Fetch results from Google Custom Search API
    results = search_google(query) if query else []
    
    # Pass the results to the template (in the 'google' section)
    return render(request, "dashboard/content.html", {"google_results": results, "query": query})


from django.shortcuts import render
from .services.google_search import search_google

import logging

logger = logging.getLogger(__name__)

def google_search_view(request):
    query = request.GET.get("q", "")
    logger.debug(f"Search Query: {query}")
    results = search_google(query) if query else []
    logger.debug(f"Search Results: {results}")
    
    return render(request, "dashboard/content.html", {"results": results, "query": query})


