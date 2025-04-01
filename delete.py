import os
from atproto import Client
from datetime import datetime

# Your Bluesky credentials
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")  # or replace with your handle
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")  # or replace with your app password

# Specify the date (YYYY-MM-DD)
TARGET_DATE = "2025-03-31"

target_date_obj = datetime.strptime(TARGET_DATE, "%Y-%m-%d").date()

client = Client()
client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)

# Fetch and delete posts
cursor = None
while True:
    feed = client.app.bsky.feed.get_author_feed({'actor': BLUESKY_HANDLE, 'limit': 100, 'cursor': cursor})
    posts = feed.feed

    if not posts:
        break

    for post in posts:
        post_date = datetime.strptime(post.post.indexed_at, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if post_date == target_date_obj:
            uri = post.post.uri
            try:
                client.delete_post(uri)
                print(f"Deleted post from {TARGET_DATE}: {uri}")
            except Exception as e:
                print(f"Error deleting post {uri}: {e}")

    cursor = feed.cursor

print(f"All posts from {TARGET_DATE} deleted.")
