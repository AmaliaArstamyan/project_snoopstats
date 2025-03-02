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
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post

# In your statistics view
def statistics(request):
    active_platform = request.GET.get('platform', 'youtube')
    top_posts = Post.objects.filter(platform=active_platform).order_by('-views')[:5]

    # Prepare the engagement data (like, shares, comments)
    post_titles = [post.title for post in top_posts]
    post_views = [post.views for post in top_posts]
    post_likes = [post.likes for post in top_posts]   # Assuming there's a `likes` field
    post_shares = [post.shares for post in top_posts]  # Assuming there's a `shares` field
    post_comments = [post.comments for post in top_posts]  # Assuming there's a `comments` field

    context = {
        'active_platform': active_platform,
        'top_posts': top_posts,
        'post_titles': post_titles,
        'post_views': post_views,
        'post_likes': post_likes,
        'post_shares': post_shares,
        'post_comments': post_comments,
    }

    return render(request, 'dashboard/statistics.html', context)


# Post_Statystics view
def poststatistics(request, post_id):
    # Fetch the specific post by its ID
    post = get_object_or_404(Post, id=post_id)

    context = {
        'post': post,  # Pass the post to the template
    }

    return render(request, 'dashboard/poststatistics.html', context)


