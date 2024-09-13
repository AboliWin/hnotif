import os
import feedparser
import sqlite3
import argparse
import logging
import sys
import time
from src.banner import banner
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import init, Fore, Back, just_fix_windows_console
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

# Import the banners from src folder banner file
banner()

# Parse the arguments
parser = argparse.ArgumentParser(
    prog='main.py',
    description='HackerNews is a tool for getting information and news from websites related to cybersecurity'
)
parser.add_argument('-s', '--silent', action='store_true', help="this option is used for just updating the database without sending notifications")
parser.add_argument('-a', '--active', action='store_true', help="when the database is updated and you want to get notifications when anything happens")

args = parser.parse_args()

while True:
    # Connect to the SQLite database
    conn = sqlite3.connect('news_feed.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS entries
                      (title TEXT, link TEXT, summary TEXT)''')

    # If -s option is used or no options are provided, just create the database
    if args.silent or not args.active:
        # Close connection without inserting or sending notifications
        conn.commit()
        conn.close()
        time.sleep(8 * 60 * 60)  # Sleep for 8 hours
        continue

    # Parse the RSS feed
    NewsFeed = feedparser.parse("http://feeds.feedburner.com/TheHackersNews")

    # Retrieve the last 20 entries
    entries = NewsFeed.entries[:20]

    # List to store new entries
    new_entries = []

    # Insert entries into the database and detect new entries
    for entry in entries:
        title = entry.title
        link = entry.link
        summary = entry.summary

        # Check if the entry already exists in the database
        cursor.execute("SELECT * FROM entries WHERE title=?", (title,))
        existing_entry = cursor.fetchone()

        # If the entry does not exist, insert it into the database and add it to new_entries list
        if not existing_entry:
            cursor.execute("INSERT INTO entries VALUES (?, ?, ?)", (title, link, summary))
            new_entries.append(entry)

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

    # Send new entries to Discord webhooks
    for entry in new_entries:
        title = entry.title
        link = entry.link
        summary = entry.summary

        # Retrieve Discord webhook URL from environment variable
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

        # Create a Discord webhook
        webhook = DiscordWebhook(url=webhook_url)

        # Create an embed
        embed = DiscordEmbed(title='New entry', description='', color=242424)
        embed.set_author(name='HackerNews', url='http://feeds.feedburner.com/TheHackersNews', icon_url='https://example.com/icon.png')
        embed.add_embed_field(name='Title', value=title)
        embed.add_embed_field(name='Link', value=link)
        embed.add_embed_field(name='Summary', value=summary)

        # Add the embed to the webhook
        webhook.add_embed(embed)

        # Send the webhook
        response = webhook.execute()

    # Sleep for 8 hours before checking again
    time.sleep(8 * 60 * 60)
