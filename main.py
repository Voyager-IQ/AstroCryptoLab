import streamlit as st
import sqlite3
import os
from scripts.gpt_analyzer import analyze_text_with_gpt
from scripts.rss_parser import parse_and_store_feeds

# --- Page Configuration ---
st.set_page_config(
    page_title="AstroCryptoLab",
    page_icon="🤖",
    layout="wide"
)

# --- Database Configuration ---
DB_PATH = os.path.join('data', 'news.db')


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    # Ensure the database and table exist before connecting
    if not os.path.exists(DB_PATH):
        st.info("Database not found. Initializing...")
        parse_and_store_feeds()
        st.success("Database initialized.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


# --- UI Components ---
st.title("🤖 KryptoGPT Trend Analyser")
st.markdown("Analyse the latest crypto news with a local Large Language Model.")

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    if st.button("Fetch Latest News"):
        with st.spinner("Fetching new articles from RSS feeds..."):
            parse_and_store_feeds()
        st.success("Feeds updated!")

    st.header("Filters")
    # Filter for analyzed/unanalyzed articles
    analysis_filter = st.radio(
        "Show articles:",
        ('All', 'Analyzed', 'Not Analyzed'),
        horizontal=True
    )

    # Text search
    search_term = st.text_input("Search in titles or summaries:")

# --- Main Application Logic ---
conn = get_db_connection()
cur = conn.cursor()

# Build the SQL query based on filters
query = "SELECT * FROM articles"
conditions = []
params = []

if analysis_filter == 'Analyzed':
    conditions.append("analyzed = 1")
elif analysis_filter == 'Not Analyzed':
    conditions.append("analyzed = 0")

if search_term:
    conditions.append("(title LIKE ? OR summary LIKE ?)")
    params.extend([f'%{search_term}%', f'%{search_term}%'])

if conditions:
    query += " WHERE " + " AND ".join(conditions)

query += " ORDER BY published_date DESC LIMIT 50"

# Fetch articles from the database
try:
    cur.execute(query, params)
    articles = cur.fetchall()
except sqlite3.Error as e:
    st.error(f"Database error: {e}")
    articles = []

if not articles:
    st.warning("No articles found matching your criteria. Try fetching the latest news or adjusting your filters.")
else:
    # Display articles in a more structured layout
    for article in articles:
        col1, col2 = st.columns([3, 2])

        with col1:
            with st.container(border=True):
                st.subheader(f"[{article['title']}]({article['link']})")
                st.caption(f"Source: **{article['source']}** | Published: {article['published_date']}")
                st.markdown(article['summary'][:400] + "..." if article['summary'] else "No summary available.")

        with col2:
            if article['analyzed']:
                with st.container(border=True):
                    st.write("✅ **Analysis Complete**")
                    st.info(f"**Sentiment:** {article['sentiment']}")
                    st.warning(f"**Mentioned Assets:** {article['mentioned_assets']}")
                    st.success(f"**Investment Signal:** {article['investment_signal']}")
            else:
                if st.button("Analyze with GPT", key=f"analyze_{article['id']}"):
                    with st.spinner("Analyzing with local GPT model... This may take a moment."):
                        analysis_result = analyze_text_with_gpt(article['summary'])

                        # Update the database with the analysis result
                        update_cur = conn.cursor()
                        update_cur.execute('''
                                           UPDATE articles
                                           SET analyzed          = 1,
                                               sentiment         = ?,
                                               mentioned_assets  = ?,
                                               investment_signal = ?
                                           WHERE id = ?
                                           ''', (
                                               analysis_result['sentiment'],
                                               analysis_result['mentioned_assets'],
                                               analysis_result['investment_signal'],
                                               article['id']
                                           ))
                        conn.commit()
                        st.rerun()  # Rerun the app to show the new analysis

conn.close()
