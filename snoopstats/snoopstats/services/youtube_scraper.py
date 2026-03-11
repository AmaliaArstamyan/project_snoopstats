import logging
import requests
from snoopstats.models import Post

logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = "AIzaSyB96wTQF0ZOcjs4jnF9kh-K4XR95x4HM6w"  # Replace with your API key
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos"

def search_youtube(query):
    """Fetch search results from YouTube Data API and save to the database."""
    if not query:
        logger.warning("Empty query passed to YouTube search.")
        return []

    params = {
        "key": YOUTUBE_API_KEY,
        "part": "snippet",
        "q": query,
        "maxResults": 10,  # Adjust the number of results
        "type": "video"
    }

    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        response.raise_for_status()
        search_results = response.json().get("items", [])

        if not search_results:
            logger.info(f"No YouTube results found for query: {query}")

        video_ids = ",".join([video["id"]["videoId"] for video in search_results])
        details_params = {
            "key": YOUTUBE_API_KEY,
            "part": "statistics",
            "id": video_ids
        }
        details_response = requests.get(YOUTUBE_VIDEO_DETAILS_URL, params=details_params)
        details_response.raise_for_status()
        video_details = {vid["id"]: vid["statistics"] for vid in details_response.json().get("items", [])}

        posts = []
        for video in search_results:
            video_id = video["id"]["videoId"]
            stats = video_details.get(video_id, {})

            post, created = Post.objects.get_or_create(
                title=video["snippet"]["title"],
                platform="youtube",
                defaults={
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "shares": 0,  # YouTube API doesn't provide share count
                    "comments": int(stats.get("commentCount", 0))
                }
            )
            posts.append(post)

        return posts

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching YouTube search results: {e}")
        return []
