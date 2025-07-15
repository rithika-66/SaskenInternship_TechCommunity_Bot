import praw
import os
from dotenv import load_dotenv

load_dotenv()  # 🔄 Load from .env

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def scrape_reddit(subreddit="learnpython", limit=20):
    results = []
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        if post.stickied:
            continue
        results.append({
            "title": post.title,
            "question": post.selftext,
            "answer": "",  # No answers from Reddit unless using comments
            "url": f"https://reddit.com{post.permalink}"
        })
    return results
