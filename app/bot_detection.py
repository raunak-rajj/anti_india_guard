import pandas as pd
from datetime import datetime


# Load dataset
df = pd.read_csv("data/sentiment_results.csv")


def get_account_age_days(created_date):
    try:
        created_dt = datetime.strptime(created_date, "%a %b %d %H:%M:%S %Y")
        today = datetime.now()
        return (today - created_dt).days
    except:
        return None


def calculate_bot_score(row):
    if not eval(str(row["anti_india_keyword"]))[0]:
        return 0, "🟢Not Applicable"

    followers = row["user_followers"] if row["user_followers"] > 0 else 1
    total_tweets = row["user_total_tweets"]
    likes = row["likes"]
    retweets = row["retweets"]
    verified = row["user_verified"]

    # Ratios
    tweet_to_follower_ratio = total_tweets / followers
    engagement_anomaly = (likes + retweets) / followers

    # Account age factor
    account_age_days = get_account_age_days(row["account_created"])
    if account_age_days is None:
        recent_account = 0
    elif account_age_days < 7:
        recent_account = 1
    elif account_age_days < 30:
        recent_account = 0.5
    else:
        recent_account = 0

    # Verified factor
    verified_factor = 1 if verified else 0

    # Weighted formula
    bot_score = (0.4 * tweet_to_follower_ratio +
                 0.2 * (1 - engagement_anomaly) +
                 0.3 * recent_account +
                 0.1 * (1 - verified_factor))

    # Normalize score (cap at 1)
    bot_score = min(bot_score, 1.0)

    label = "🔴Bot Suspected" if bot_score >= 0.7 else "🔵Likely Human"
    return bot_score, label

# === Apply to dataset ===
df["bot_score"], df["bot_label"] = zip(*df.apply(calculate_bot_score, axis=1))

# === Save new CSV ===
df.to_csv("data/bot_suspected.csv", index=False)

print("Bot detection results saved to bot_suspected.csv")
