# services/google_search.py
import logging
import requests
from snoopstats.models import Post

logger = logging.getLogger(__name__)

GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
GOOGLE_API_KEY = "AIzaSyB96wTQF0ZOcjs4jnF9kh-K4XR95x4HM6w"  #  API key
SEARCH_ENGINE_ID = "028f95e95198d4a93"  #  search engine ID

def search_google(query):
    """Fetch search results from Google Custom Search API and save to the database."""
    if not query:
        logger.warning("Empty query passed to Google search.")
        return []

    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query
    }

    try:
        response = requests.get(GOOGLE_SEARCH_URL, params=params)
        response.raise_for_status()  # Raises an exception for 4xx/5xx status codes

        logger.debug(f"Google Search API response status: {response.status_code}")
        search_results = response.json().get("items", [])
        
        if not search_results:
            logger.info(f"No results found for query: {query}")

        # Save search results to the database
        posts = []
        for result in search_results:
            post, created = Post.objects.get_or_create(
                title=result.get("title", ""),
                platform="google",  # Set the platform here
                defaults={
                    "views": result.get("views", 0),  # Example data, replace with actual field if available
                    "likes": result.get("likes", 0),
                    "shares": result.get("shares", 0),
                    "comments": result.get("comments", 0)
                }
            )
            posts.append(post)
        
        return posts

    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while making the request to Google Search API: {e}")
        return []

    except ValueError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return []
