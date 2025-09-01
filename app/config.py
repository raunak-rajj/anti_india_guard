"""
Configuration file for Twitter sentiment analysis
"""

# Twitter Search Configuration
SEARCH_QUERIES = [
    "India OR #India",
    "Indian OR #Indian", 
    "Hindu OR #Hindu",
    "Kashmir OR #Kashmir"
]

# Anti-India Keywords for Sentiment Detection
ANTI_INDIA_KEYWORDS = [
    "hate india", "fuck india", "anti india", "india bad", "india terrorist",
    "dirty india", "poor india", "india scam", "corrupt india", "india is corrupt", "india fake",
    "hindustan murdabad", "down with india", "destroy india", "bomb india",
    "kashmir freedom", "free kashmir", "india occupation", "india fascist",
    "modi dictator", "hindu terrorist", "hindu nationalism", "india propaganda", "boycott india"
]

# CSV Configuration
RAW_DATA_CSV = "data/raw_tweets.csv"
FLAGGED_DATA_CSV = "data/flagged_tweets.csv"
DATA_DIR = "data"

# Hugging Face Model
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
