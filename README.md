# GitHub Monitoring and Dashboard Application

### For complete tutorial till deployment on youtube video :

[![YouTube Video](https://img.youtube.com/vi/UODhykaY6WI/0.jpg)](https://www.youtube.com/watch?v=UODhykaY6WI&t=0s)

This project monitors GitHub repositories for recent commits and visualizes the data through a dashboard. It consists of two main components:

- **Dashboard Connection (`database.py`)**
- **Commit Monitor (`fetch_commit.py`)**
- **Dashboard Application (`dashboard.py`)**

---
## Database Connection (`database.py`)

### Purpose
Check the connection is established or not with database.

### How It Works
1. **Fetch Commits:**
   - Uses the Database API to check connection.


## Commit Monitor (`github_monitor.py`)

### Purpose
The commit monitor fetches recent commits from specified GitHub repositories and stores them in a MongoDB database. It runs continuously, checking for new commits every hour.

### How It Works
1. **Fetch Commits:**
   - Uses the GitHub API to fetch commits made in the last hour.
   - Filters duplicates to avoid redundant storage.

2. **Store in MongoDB:**
   - Saves commit details (e.g., message, author, date, URL) in a MongoDB collection.
   - Each commit is uniquely identified using its URL.

3. **Schedule Monitoring:**
   - Runs every hour using a `while` loop with `time.sleep()`.

### Why Use It?
- To monitor competitor or important repositories for changes.
- Useful for tracking activity trends and staying updated on new updates or changes.

### Run the Script:
```bash
python fetch_commit.py
```

# GitHub Monitoring Dashboard Application

The GitHub Monitoring Dashboard visualizes commit activity stored in a MongoDB database. It provides insights into recent commits and trends across specified GitHub repositories.

---

## Purpose
The dashboard offers an interactive interface to:
- Display recent commit details (author, date, message, etc.).
- Visualize commit activity trends through charts.

---

## How It Works

### 1. **Fetch Data**
- Connects to a MongoDB database.
- Retrieves commit data and loads it into a pandas DataFrame.

### 2. **Display Commit Data**
- Renders a table showing recent commit information such as:
  - **Author**
  - **Commit Message**
  - **Commit Date**
  - **URL**

### 3. **Visualize Trends**
- Groups commit activity by date.
- Displays a bar chart of daily commit counts.


## Why Use It?

### Gain Insights:
- Analyze commit activity trends.
- Monitor productivity and peak activity times.

### Team Collaboration:
- Track contributions across repositories in a team or organization.

### Competitor Analysis:
- Visualize activity patterns in competitor repositories.

---

## How to Run the Dashboard

1. **Ensure MongoDB is set up and populated with commit data** (via the `fetch_commit.py` script).

2. **Run the Dashboard**:
   ```bash
   streamlit run dashboard.py
```
