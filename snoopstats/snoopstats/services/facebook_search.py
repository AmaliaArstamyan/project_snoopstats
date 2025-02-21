import logging
import requests
from snoopstats.models import Post

logger = logging.getLogger(__name__)

FACEBOOK_ACCESS_TOKEN = "EAAQbrFUXyZBMBO1IY4kJpZAQOpFkYB7CK8Wgl3pt6XEfpZBc4W1eZCRSe5OcHZBNeDT0EgM3Iqg9oHD11evS0wnOUGjZBM8GcT28DBBkavpznw2UzzeQbdKBDBB3MHmnj8dZCPJQqbAzCssK8J6wq2hWhHBrl7UVNJxnrOT9ZCIeydZBskh1Il0nRBJNu"
FACEBOOK_GRAPH_API_URL = "https://graph.facebook.com/v19.0/search"

def search_facebook(query):
    """Fetch search results from Facebook Graph API and save to the database."""
    if not query:
        logger.warning("Empty query passed to Facebook search.")
        return []

    params = {
        "q": query,
        "type": "post",
        "access_token": FACEBOOK_ACCESS_TOKEN,
        "fields": "message,likes.summary(true),shares,comments.summary(true)"
    }

    try:
        response = requests.get(FACEBOOK_GRAPH_API_URL, params=params)
        response.raise_for_status()
        search_results = response.json().get("data", [])

        if not search_results:
            logger.info(f"No Facebook results found for query: {query}")

        posts = []
        for post_data in search_results:
            post, created = Post.objects.get_or_create(
                title=post_data.get("message", "Untitled Post"),
                platform="facebook",
                defaults={
                    "likes": post_data.get("likes", {}).get("summary", {}).get("total_count", 0),
                    "shares": post_data.get("shares", {}).get("count", 0),
                    "comments": post_data.get("comments", {}).get("summary", {}).get("total_count", 0),
                    "views": 0  # Facebook API doesn't provide views
                }
            )
            posts.append(post)

        return posts

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Facebook search results: {e}")
        return []
