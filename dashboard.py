import streamlit as st
import pandas as pd
from database import get_mongo_client

# Fetch Data from MongoDB
def fetch_data():
    client = get_mongo_client()
    data = list(client.find({}, {"_id": 0}))  # Exclude MongoDB's ObjectId
    return pd.DataFrame(data)

# Streamlit App
st.set_page_config(page_title="GitHub Monitoring Dashboard", layout="wide")  # Improved layout

st.title("GitHub Monitoring Dashboard")
st.markdown("View and analyze GitHub commit activity from monitored repositories.")

with st.spinner("Loading data..."):
    commits_data = fetch_data()

if not commits_data.empty:
    # Convert date column to datetime for filtering and visualization
    commits_data["date"] = pd.to_datetime(commits_data["date"])

    # Overview Table
    st.subheader("Recent Commits Overview")
    with st.expander("Show/Hide Raw Data"):
        st.dataframe(commits_data, use_container_width=True)

    # Filters
    st.sidebar.header("Filters")
    repo_filter = st.sidebar.multiselect(
        "Select Repositories",
        options=commits_data["repo"].unique(),
        default=commits_data["repo"].unique(),
    )
    author_filter = st.sidebar.text_input("Filter by Author (Case-insensitive):").lower()

    # Apply Filters
    filtered_data = commits_data[
        (commits_data["repo"].isin(repo_filter)) &
        (commits_data["author"].str.lower().str.contains(author_filter, na=False))
    ]

    # Show Filtered Data
    st.subheader("Filtered Commits Overview")
    if not filtered_data.empty:
        st.dataframe(filtered_data, use_container_width=True)
    else:
        st.warning("No data matching the filters!")

    # Visualization
    st.subheader("Commit Activity Over Time")
    if not filtered_data.empty:
        chart_data = filtered_data.groupby(filtered_data["date"].dt.date).size()
        st.line_chart(chart_data, use_container_width=True)

    # Commit Count by Author
    st.subheader("Commit Count by Author")
    if not filtered_data.empty:
        author_chart_data = filtered_data["author"].value_counts()
        st.bar_chart(author_chart_data, use_container_width=True)
else:
    st.warning("No data found in the database!")