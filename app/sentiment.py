from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import pandas as pd
from config import ANTI_INDIA_KEYWORDS
from clean_text import clean_data

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
ROBERTA_SUPPORTED_LANGUAGES = ('ar', 'en', 'fr', 'de', 'hi', 'it', 'es', 'pt')

model = AutoModelForSequenceClassification.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)


# save the model locally
model.save_pretrained(MODEL)
tokenizer.save_pretrained(MODEL)


def predict_sentiment(text: str) -> str:
    clean_text = clean_data(text)
    encoded_input = tokenizer(
        clean_text,
        return_tensors='pt',
        truncation=True,   
        max_length=512 
        )
    output = model(**encoded_input)
    index_of_sentiment = output.logits.argmax().item()
    sentiment = config.id2label[index_of_sentiment]
    return sentiment


def find_anti_india_keyword(text: str) -> str:
    clean_text = clean_data(text)
    matched = [k for k in ANTI_INDIA_KEYWORDS if k.replace(" ", "") in clean_text.replace(" ", "")]
    return bool(matched), matched


# Load your CSV file
df = pd.read_csv("data/translated_tweets.csv")  

# Normalize column names to lowercase for compatibility
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Apply the sentiment prediction function
df['sentiment'] = df['cleaned_text'].apply(predict_sentiment)

# Anti-India keyword match column
df['anti_india_keyword'] = df['cleaned_text'].apply(find_anti_india_keyword)

# Save the results to a new CSV (optional)
df.to_csv("data/sentiment_results.csv", index=False)

print("Sentiment results saved to sentiment_results.csv")
