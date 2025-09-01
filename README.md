# anti_india_guard


This project analyzes social media data to detect **anti-India posts**, perform **sentiment analysis**, and identify whether accounts are **bots or humans**.  
It provides **interactive visualizations** using **Streamlit** and **Plotly**.

---

##  Features

- **Sentiment Analysis**
  - Classifies posts into sentiment categories (Positive, Neutral, Negative).
  - Histogram visualization shows sentiment distribution in **percentages**.

- **Anti-India Content Detection**
  - Custom keyword-based detection function:
  - Counts and highlights anti-India posts.
  - Bar chart visualization with proportion of total posts.

- **Bot vs Human Classification**
  - Detects if a user is likely a bot or human.
  - Donut pie chart visualization of bot-human distribution.

- **Interactive Dashboards**
  - Built using **Streamlit** and **Plotly** for real-time, interactive charts.

---

##  Visualizations

- Sentiment distribution (percentages).  
- Anti-India posts (bar chart with counts + percentage).  
- Bot vs Human distribution (donut pie chart).  

---

##  Tech Stack

- **Python**
- **Pandas** (data processing)
- **Plotly Express** (interactive charts)
- **Streamlit** (dashboard & UI)

---

##  NLP model

- "cardiffnlp/twitter-roberta-base-sentiment-latest"


##  Requirements

Create a virtual environment and install dependencies:

##  How to Run

1. Install **Python 3.9+**  
   - [Download Python](https://www.python.org/downloads/) and make sure it is added to your PATH.  
   - Verify installation:
     ```bash
     python --version
     ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   ```

   ```bash
   source venv/bin/activate     # On macOS/Linux
   ```
   
   ```bash
   venv\Scripts\activate        # On Windows
   ```
   ```bash
   pip install -r requirements.txt
   ```

3. Pre-download the RoBERTa sentiment model (so app doesn’t hang later)
   ```bash
   python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
   AutoTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment-latest'); \
   AutoModelForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment-latest')"
   ```

4. Run the web app:
   ```bash
   streamlit run app/demo_app.py
   ```