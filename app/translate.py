# translate.py

import pandas as pd
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0

def translate_text(text: str) -> str:
    """
    Translate any non-English text into English.
    """
    try:
        lang = detect(text)
    except:
        lang = "en"  # fallback if detection fails
    
    if lang != "en":
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except Exception as e:
            print(f"Translation failed for: {text}. Error: {e}")
            return text
    else:
        return text

if __name__ == "__main__":

    # Load CSV    
    df = pd.read_csv("data/cleaned_tweets.csv")

    # Normalize column names to lowercase for compatibility
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    if 'text' not in df.columns:
        raise ValueError("CSV must have a 'text' column containing the texts to translate.")
    
    # Translate texts
    df['translated_text'] = df['cleaned_text'].apply(translate_text)
    
    # Save results
    df.to_csv("data/translated_tweets.csv", index=False)
    
    print("Translated tweets saved to translated_data.csv")
