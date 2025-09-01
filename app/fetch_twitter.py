import asyncio
import os
import csv
from datetime import datetime
from twikit import Client
from config import SEARCH_QUERIES, RAW_DATA_CSV, DATA_DIR

COOKIES_FILE = "twitter_cookies.json"


def format_date(dt):

    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    try:

        parsed = datetime.strptime(str(dt), "%a %b %d %H:%M:%S %z %Y")
        return parsed.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(dt)  


async def scrap_tweets():
    client = Client('en-US')

    # Login using cookies if available, else ask credentials once
    if os.path.exists(COOKIES_FILE):
        client.load_cookies(COOKIES_FILE)
    else:
        username = input("Username/Email: ").strip()
        password = input("Password: ").strip()
        await client.login(auth_info_1=username, password=password)
        client.save_cookies(COOKIES_FILE)


    # Ensure data dir exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Write header only if file doesn’t exist
    write_header = not os.path.exists(RAW_DATA_CSV)

    count = 0
    if os.path.exists(RAW_DATA_CSV):
        with open(RAW_DATA_CSV, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                count = int(rows[-1][0])  # last count in CSV

    with open(RAW_DATA_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                  "count", "id", "username", "text", "likes", "retweets", "replies", 
                  "user_followers", "user_total_tweets", "post_created", "user_verified", "account_created",
                  "engagement_score", "link"
            ])

        
        for query in SEARCH_QUERIES:
            tweets = await client.search_tweet(query, product="Top")

            for t in tweets[:150]: 
                user_verified = (
                getattr(t.user, "verified", False) 
                or getattr(t.user, "is_blue_verified", False) 
                or (hasattr(t.user, "badges") and "verified" in t.user.badges)
                )

                count += 1
                writer.writerow([
                     count,
                     t.id,
                     t.user.screen_name,
                     t.full_text.replace("\n", " "),
                     t.favorite_count or 0,
                     t.retweet_count or 0,
                     t.reply_count or 0,
                     t.user.followers_count or 0,
                     t.user.statuses_count or 0,
                     format_date(t.created_at),        
                     user_verified,
                     format_date(t.user.created_at),    
                     (t.favorite_count or 0) + (t.retweet_count or 0) + (t.reply_count or 0),

                    f"https://twitter.com/{t.user.screen_name}/status/{t.id}",
                    
                ])



if __name__ == "__main__":
    asyncio.run(scrap_tweets())
    print(f"Scraped tweets saved to {RAW_DATA_CSV}")

