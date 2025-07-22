import feedparser
import sqlite3
import os
from dateutil.parser import parse as parse_date

# Define the path for the database relative to the project root
DB_PATH = os.path.join('data', 'news.db')
FEED_FILE = 'feeds.txt'


def get_source_name(url):
    """Extracts a readable source name from the feed URL."""
    if 'coindesk' in url:
        return 'CoinDesk'
    if 'cointelegraph' in url:
        return 'CoinTelegraph'
    if 'reuters' in url:
        return 'Reuters'
    if 'ft.com' in url:
        return 'Financial Times'
    return 'Unknown Source'


def create_database():
    """Creates the database and the articles table if they don't exist."""
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table with the new, more detailed schema
    cur.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        published_date TEXT,
        summary TEXT,
        source TEXT,
        analyzed INTEGER DEFAULT 0,
        sentiment TEXT,
        mentioned_assets TEXT,
        investment_signal TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("Database created/ensured successfully.")


def parse_and_store_feeds():
    """Parses RSS feeds from a file and stores new entries in the database."""
    create_database()  # Ensure DB and table exist before parsing

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        with open(FEED_FILE, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: '{FEED_FILE}' not found. Please create it and add RSS feed URLs.")
        return

    new_entries_count = 0
    for url in urls:
        print(f"Parsing feed: {url}")
        feed = feedparser.parse(url)
        source_name = get_source_name(url)

        for entry in feed.entries:
            # Use a tuple for the query to prevent SQL injection
            cur.execute("SELECT id FROM articles WHERE link = ?", (entry.link,))
            if cur.fetchone() is not None:
                # Skip if the article link already exists
                continue

            # Safely get attributes
            title = entry.get('title', 'No Title')
            link = entry.get('link', '')
            summary = entry.get('summary', 'No Summary')

            # Parse date safely
            published = entry.get('published', '')
            try:
                # Format date to a consistent ISO 8601 format
                published_iso = parse_date(published).isoformat() if published else None
            except Exception:
                published_iso = None  # Or keep the original string: published

            # Insert new entry
            cur.execute('''
            INSERT INTO articles (title, link, published_date, summary, source)
            VALUES (?, ?, ?, ?, ?)
            ''', (title, link, published_iso, summary, source_name))
            new_entries_count += 1

    conn.commit()
    conn.close()
    print(f"Finished parsing. Added {new_entries_count} new articles to the database.")


if __name__ == '__main__':
    # This allows the script to be run directly to update the feeds
    parse_and_store_feeds()
