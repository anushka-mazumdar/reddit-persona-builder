import requests
import json
import time
from datetime import datetime
import os

USER_AGENT = "Mozilla/5.0 (compatible; RedditScraper/1.0; +https://github.com/yourusername)"
HEADERS = {"User-Agent": USER_AGENT}

def fetch_reddit_data(username, data_type="overview", after=None):
    url = f"https://www.reddit.com/user/{username}/{data_type}.json"
    params = {"limit": 100}
    if after:
        params["after"] = after
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch {data_type}: {response.status_code}")
        return None

def is_relevant_subreddit(subreddit):
    if subreddit is None:
        return False
    irrelevant = {"memes", "dankmemes", "funny", "AdviceAnimals"}
    return subreddit.lower() not in irrelevant

def parse_item(item):
    kind = item["kind"]
    data = item["data"]
    if kind == "t1":  # Comment
        return {
            "type": "comment",
            "subreddit": data.get("subreddit"),
            "body": data.get("body"),
            "created_utc": data.get("created_utc"),
            "score": data.get("score"),
            "permalink": f"https://www.reddit.com{data.get('permalink')}",
            "parent_id": data.get("parent_id"),
            "link_title": data.get("link_title"),
        }
    elif kind == "t3":  # Submission
        return {
            "type": "post",
            "subreddit": data.get("subreddit"),
            "title": data.get("title"),
            "selftext": data.get("selftext"),
            "created_utc": data.get("created_utc"),
            "score": data.get("score"),
            "permalink": f"https://www.reddit.com{data.get('permalink')}",
            "url": data.get("url"),
        }
    return None

def scrape_user(username):
    all_items = []
    after = None
    while True:
        data = fetch_reddit_data(username, "overview", after)
        if not data or "data" not in data or not data["data"]["children"]:
            break
        for item in data["data"]["children"]:
            parsed = parse_item(item)
            if parsed and is_relevant_subreddit(parsed.get("subreddit")):
                all_items.append(parsed)
        after = data["data"].get("after")
        if not after:
            break
        time.sleep(1)
    all_items.sort(key=lambda x: x["created_utc"])
    for item in all_items:
        item["datetime"] = datetime.utcfromtimestamp(item["created_utc"]).isoformat() + "Z"
    return all_items

def save_user_data(username, data):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{username}_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} items to data/{username}_raw.json")

# Run this script directly
if __name__ == "__main__":
    username = 'username_here'  # Replace with the Reddit username you want to scrape
    print(f"Scraping Reddit data for user: {username}")
    data = scrape_user(username)
    save_user_data(username, data)
