import os
import requests
import pytz
from datetime import datetime, timedelta
import time
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = "Github_Commits"
COLLECTION_NAME = "Commits"
TOKEN = os.getenv("GIT_TOKEN")

Base_url = "https://api.github.com"

# MongoDB connection
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    commits_collection = db[COLLECTION_NAME]
    print("MongoDB connection established.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

# Headers for authorization
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Repositories to monitor
repositories = [
    {"owner": "langflow-ai", "repo": "langflow"},
    {"owner": "freeCodeCamp", "repo": "freeCodeCamp"},
    {"owner": "tensorflow", "repo": "tensorflow"},
]

# Convert UTC to IST
def get_ist_time(utc_time):
    try:
        ist = pytz.timezone('Asia/Kolkata')
        return utc_time.astimezone(ist)
    except Exception as e:
        print(f"Error converting time to IST: {e}")
        return utc_time

# Fetch recent commits with error handling
def fetch_recent_commits(owner, repo):
    try:
        url = f"{Base_url}/repos/{owner}/{repo}/commits"
        params = {"since": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"}
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            commits = response.json()
            for commit in commits:
                try:
                    commit_data = {
                        "repo": repo,
                        "commit_message": commit["commit"]["message"],
                        "author": commit["commit"]["author"]["name"],
                        "date": commit["commit"]["author"]["date"],
                        "url": commit["html_url"],
                        "fetched_at": get_ist_time(datetime.utcnow())
                    }
                    # Avoid duplicates
                    if not commits_collection.find_one({"url": commit["html_url"]}):
                        commits_collection.insert_one(commit_data)
                        print(f"Stored commit: {commit['commit']['message']} from {repo}")
                    else:
                        print(f"Duplicate commit skipped: {commit['html_url']}")
                except Exception as e:
                    print(f"Error processing commit: {e}")
        else:
            print(f"Failed to fetch commits for {repo}. HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"Error fetching commits for {owner}/{repo}: {e}")

# Monitor all repositories
def monitor_repositories():
    print(f"Monitoring repositories at {get_ist_time(datetime.utcnow())} (IST)...\n")
    for repo in repositories:
        try:
            print(f"Fetching commits for {repo['repo']}...")
            fetch_recent_commits(repo["owner"], repo["repo"])
        except Exception as e:
            print(f"Error monitoring repository {repo['repo']}: {e}")
    print("\nMonitoring cycle completed.\n")

if __name__ == "__main__":
    while True:
        try:
            monitor_repositories()
            time.sleep(3600)  # Run every hour
        except KeyboardInterrupt:
            print("Monitor stopped by user.")
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
