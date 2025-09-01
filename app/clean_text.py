import pandas as pd
import re

# Your cleaning function
def clean_data(text):
    text = re.sub(r"@", "", text)  # Remove mentions
    text = re.sub(r"https?://\S+|www\.\S+", "", text)  # Remove URLs
    text = re.sub(r"#", "", text)  # Remove only the '#' symbol
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text.lower()

# Load CSV
df = pd.read_csv("data/dummy_tweets.csv")  # replace with your file name

# Normalize column names to lowercase for compatibility
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Apply cleaning function to the column
df["cleaned_text"] = df["text"].astype(str).apply(clean_data)


# Save the cleaned data back to CSV
df.to_csv("data/cleaned_tweets.csv", index=False) 

print("Cleaned tweets saved to cleaned_tweets.csv")