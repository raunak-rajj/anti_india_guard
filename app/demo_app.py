import streamlit as st
import pandas as pd
import subprocess
import os
import sys
import time
import asyncio
from twikit import Client
import plotly.express as px

# Paths to CSV files

COOKIES_FILE = "twitter_cookies.json" 

# Configure Streamlit page
st.set_page_config(
    page_title="ANTI_INDIA_GUARD - Data Processing Pipeline",
    page_icon="🛡️",
    layout="wide",
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: #f8fafc;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }

    .main-header h3 {
        font-weight: 500;
        color: #cbd5e1;
    }

    /* Step Card */
    .step-card {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.25);
        margin-bottom: 1.2rem;
        border-left: 5px solid #60a5fa;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: #e2e8f0;
    }

    .step-card:hover {
        background: rgba(30, 41, 59, 0.95);
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }

    /* Status Colors */
    .success-status {
        color: #22c55e;
        font-weight: bold;
    }

    .error-status {
        color: #ef4444;
        font-weight: bold;
    }

    .processing-status {
        color: #3b82f6;
        font-weight: bold;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 18px rgba(124, 58, 237, 0.45);
    }

    /* Tabs & Dataframe */
    .stTabs [role="tablist"] {
        gap: 1rem;
    }

    .stTabs [role="tab"] {
        background: #1e293b;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        color: #e2e8f0;
        transition: background 0.3s ease;
    }

    .stTabs [role="tab"]:hover {
        background: #334155;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: #fff;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #60a5fa;
        font-weight: 700;
        font-size: 1.3rem;
    }

    /* Divider Styling */
    .stDivider {
        border-top: 2px solid #334155;
        margin: 2rem 0;
    }
</style>

""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline_status' not in st.session_state:
    st.session_state.pipeline_status = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'csv_files' not in st.session_state:
    st.session_state.csv_files = {}

# Pipeline configuration - adjust paths to match your project structure
PIPELINE_STEPS = [
    {
        'name': 'Fetch Twitter Data',
        'file': 'app/fetch_twitter.py',
        'description': 'Fetches Twitter data using API',
        'output_csv': 'data/raw_tweets.csv'
    },
    {
        'name': 'Generate Dummy Tweets',
        'file': 'app/dummy_tweets.py',
        'description': 'Generates additional dummy tweet data',
        'output_csv': 'data/dummy_tweets.csv'
    },
    {
        'name': 'Clean Text',
        'file': 'app/clean_text.py',
        'description': 'Cleans and preprocesses tweet text',
        'output_csv': 'data/cleaned_tweets.csv'
    },
    {
        'name': 'Translate Text',
        'file': 'app/translate.py',
        'description': 'Translates non-English tweets to English',
        'output_csv': 'data/translated_tweets.csv'
    },
    {
        'name': 'Sentiment & Anti India Posts',
        'file': 'app/sentiment.py',
        'description': 'Performs sentiment analysis and detect Anti India posts on tweets',
        'output_csv': 'data/sentiment_results.csv'
    },
    {
        'name': 'Bot Detection',
        'file': 'app/bot_detection.py',
        'description': 'Detects potential bot accounts',
        'output_csv': 'data/bot_suspected.csv'
    }
]

def run_python_script(script_path, args=None):
    """Run a Python script with optional arguments and return the result"""
    try:
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)  # Add arguments like ["Latest"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# Sidebar: Twitter credentials (only if cookies missing)
with st.sidebar:
    st.header("🔑 Twitter Login")

    def _do_login(u: str, p: str):
        async def _login():
            client = Client('en-US')
            await client.login(auth_info_1=u, password=p)
            client.save_cookies(COOKIES_FILE)
        asyncio.run(_login())

    if not os.path.exists(COOKIES_FILE):
        st.warning("No cookies found. Please log in once to save cookies.")
        username = st.text_input("Username / Email", key="twitter_username")
        password = st.text_input("Password", type="password", key="twitter_password")

        colA, colB = st.columns(2)
        if colA.button("🔐 Login & Save Cookies"):
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                try:
                    _do_login(username, password)
                    st.success("✅ Logged in. Cookies saved.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

        with colB:
            st.caption("First-time login only. After this, cookies will be used automatically.")
    else:
        st.success("✅ Cookies found. You’re logged in.")
        if st.button("🗑️ Clear Cookies (Log out)"):
            try:
                os.remove(COOKIES_FILE)
                st.info("Cookies removed. Please log in again.")
                st.rerun()
            except Exception as e:
                st.error(f"Couldn't remove cookies: {e}")



# Function to load CSV files

def load_csv_file(file_path):
    """Load CSV file if it exists"""
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"Error loading CSV file: {str(e)}")
            return None
    return None

# Main header
st.markdown("""
<div class="main-header">
    <h1>🛡️ ANTI_INDIA_GUARD</h1>
    <h3>Data Processing Pipeline Dashboard</h3>
    <p>Monitor and execute your data processing workflow step by step</p>
</div>
""", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🚀 Pipeline Execution")
    
   

    col3, col4 = st.columns([1, 1])

    with col3:
    # Run all steps button
     if st.button("▶️ Run Pipeline", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, step in enumerate(PIPELINE_STEPS):
            status_text.text(f"Running: {step['name']}")
            st.session_state.pipeline_status[i] = 'processing'
            
            # Run the actual Python script
            success, stdout, stderr = run_python_script(step['file'])
            
            if success:
                st.session_state.pipeline_status[i] = 'completed'
                # Load the generated CSV
                df = load_csv_file(step['output_csv'])
                if df is not None:
                    st.session_state.csv_files[i] = df
                st.success(f"✅ {step['name']} completed")
                if stdout:
                    st.code(stdout, language="text")
            else:
                st.session_state.pipeline_status[i] = 'error'
                st.error(f"❌ Error in {step['name']}")
                if stderr:
                    st.code(stderr, language="text")
            
            progress_bar.progress((i + 1) / len(PIPELINE_STEPS))
            time.sleep(0.5)  # Small delay for visualization
        
        status_text.text("Pipeline completed!")
        st.rerun()
    
    st.divider()

    with col4:
    # Reset pipeline button
     if st.button("🔄 Reset Pipeline", type="secondary"):
        st.session_state.pipeline_status = {}
        st.session_state.current_step = 0
        st.session_state.csv_files = {}
        st.rerun()
    
    # Individual step buttons
    st.subheader("Individual Steps")

    for i, step in enumerate(PIPELINE_STEPS):
      with st.container():
         st.markdown(f"""
         <div class="step-card">
               <h4>{step['name']}</h4>
               <p>{step['description']}</p>
         </div>
         """, unsafe_allow_html=True)
         
         status = st.session_state.pipeline_status.get(i, 'pending')

         # Show status
         if status == 'completed':
               st.markdown('<p class="success-status">✅ Completed</p>', unsafe_allow_html=True)
         elif status == 'processing':
               st.markdown('<p class="processing-status">⏳ Processing...</p>', unsafe_allow_html=True)
         elif status == 'error':
               st.markdown('<p class="error-status">❌ Error</p>', unsafe_allow_html=True)
         
         # Enable only if first step OR previous step is completed
         disabled = False
         if i > 0 and st.session_state.pipeline_status.get(i-1) != "completed":
               disabled = True
         
         if st.button(f"Run {step['name']}", key=f"run_{i}", disabled=disabled):
               st.session_state.pipeline_status[i] = 'processing'
               with st.spinner(f"Running {step['name']}..."):
                  success, stdout, stderr = run_python_script(step['file'])

                  if success:
                     st.session_state.pipeline_status[i] = 'completed'
                     st.success(f"{step['name']} completed successfully!")

                     # Load the generated CSV
                     df = load_csv_file(step['output_csv'])
                     if df is not None:
                           st.session_state.csv_files[i] = df
                           st.info(f"Generated: {step['output_csv']}")

                     # Show stdout if available
                     if stdout.strip():
                           with st.expander("View Output"):
                              st.code(stdout, language="text")

                  else:
                     st.session_state.pipeline_status[i] = 'error'
                     st.error(f"Error running {step['name']}")
                     if stderr:
                           st.code(stderr, language="text")
               
               # Optional: refresh UI after update
               st.rerun()

INTERMEDIATE_CSVS = [
    "data/raw_tweets.csv",
    "data/dummy_tweets.csv",        
    "data/cleaned_tweets.csv",        
    "data/translated_tweets.csv",        
    "data/sentiment_results.csv",
    "data/bot_suspected.csv", 
    "data/anti_india_flagged.csv"            
]

# Data display and download section

with col2:
    col5, col6 = st.columns([3, 1])
    with col5:
        st.header("📄 Generated Data Files")
    with col6:
        def clear_intermediate_csvs():
            deleted_files = []
            for file in INTERMEDIATE_CSVS:
                if os.path.exists(file):
                    os.remove(file)
                    deleted_files.append(file)
            return deleted_files

        if st.button("Clear CSVs"):
            deleted = clear_intermediate_csvs()
            placeholder = st.empty()
            if deleted:
                placeholder.success(f"Deleted files: {', '.join(deleted)}")
            else:
                placeholder.info("No intermediate CSV files found to delete.")
            time.sleep(2)
            placeholder.empty()

 # Display tabs for each completed step with data

    if st.session_state.csv_files:
        tabs = st.tabs([f"Step {i+1}: {PIPELINE_STEPS[i]['name']}" for i in st.session_state.csv_files.keys()])
        for tab_idx, (step_idx, df) in enumerate(st.session_state.csv_files.items()):
            with tabs[tab_idx]:
                step = PIPELINE_STEPS[step_idx]
                st.subheader(f"📊 {step['name']} Results")
                st.caption(f"File: {step['output_csv']}")
                col_info1, col_info2 = st.columns(2)
                with col_info1: st.metric("Tweets_Count", len(df))
                with col_info2: st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                show_df = df.copy()

               # Ensure link column exists and is clean
                if "link" in show_df.columns:
                  show_df["link"] = show_df["link"].fillna("")

                  st.dataframe(
                     show_df,
                     use_container_width=True,
                     height=400,
                     column_config={
                           "link": st.column_config.LinkColumn("link", display_text="🔗 Go to Post")
                     }
                  )
                else:
                  st.dataframe(show_df, use_container_width=True, height=400)

                csv_data = df.to_csv(index=False)
                st.download_button(
                    label=f"📥 Download {step['output_csv'].split('/')[-1]}",
                    data=csv_data,
                    file_name=step['output_csv'].split('/')[-1],
                    mime="text/csv"
                )
               
    else:
        st.info("👈 Run pipeline steps to generate and view CSV files here")
        st.subheader("Expected Outputs")
        for i, step in enumerate(PIPELINE_STEPS):
            with st.expander(f"Step {i+1}: {step['name']}"):
                st.write(f"**Description:** {step['description']}")
                st.write(f"**Output File:** `{step['output_csv']}`")


   #  Analytics & Alerts Section

    st.header("📊 Analytics & Alerts")

      # Show analytics only if Bot Detection step is completed
    bot_step_index = next(
         (i for i, step in enumerate(PIPELINE_STEPS) if step["name"] == "Bot Detection"), None
      )

    if bot_step_index is not None and st.session_state.pipeline_status.get(bot_step_index) == "completed":
         final_df = st.session_state.csv_files.get(bot_step_index)

         if final_df is not None and not final_df.empty:
            
            # Create two columns
            col7, col8 = st.columns(2)


            with col7:
               # Sentiment distribution with % labels
               sentiment_counts = final_df["sentiment"].value_counts().reset_index()
               sentiment_counts.columns = ["sentiment", "count"]
               sentiment_counts["percent"] = sentiment_counts["count"] / sentiment_counts["count"].sum()

               fig_Sentiment = px.bar(
                  sentiment_counts,
                  x="sentiment",
                  y="count",
                  color="sentiment",
                  text=sentiment_counts.apply(lambda row: f"{row['count']} ({row['percent']:.1%})", axis=1),
                  title="Sentiment Distribution"
               )

               fig_Sentiment.update_traces(textposition="outside")

               fig_Sentiment.update_layout(
                  yaxis_title="Count",
                  xaxis_title="Sentiment",
                  showlegend=False,
                  bargap=0.5
               )

               st.plotly_chart(fig_Sentiment, use_container_width=True)


            with col8:
               # 2. Anti-India Posts Count
               final_df["anti_india_flag"] = final_df["anti_india_keyword"].apply(lambda x: eval(str(x))[0])
               anti_count = final_df["anti_india_flag"].sum()   # number of True
               total_count = len(final_df)

               # Use numeric value for bar height
               fig_anti_bar = px.bar(
                  x=["Anti-India Posts"],
                  y=[anti_count],
                  color_discrete_map={"Anti-India Posts": "red"},
                  text=[f"{anti_count} ({anti_count/total_count:.1%})"]  # show formatted text on bar
               )

               fig_anti_bar.update_traces(
                  textposition="outside",
                  width=0.3 
               )

               fig_anti_bar.update_layout(
                  showlegend=False,
                  yaxis_title="Count",
                  xaxis_title=None,
                  bargap=0.6  
               )

               st.plotly_chart(fig_anti_bar, use_container_width=True)

         
            # 3. Bot vs Human Pie Chart 
            fig_bot = px.pie(
               final_df,
               names="bot_label",
               title="Bot vs Human Distribution",
               hole=0.3
            )
            st.plotly_chart(fig_bot, use_container_width=True)
            
    else:
         st.info("Analytics available only after completing the 'Bot Detection' step in this session.")

# 🚨 Anti-India Alert Section
st.header("🚨 Anti-India Posts Report")

if bot_step_index is not None and st.session_state.pipeline_status.get(bot_step_index) == "completed":
    final_df = st.session_state.csv_files.get(bot_step_index)

    if final_df is not None and not final_df.empty:
        flagged_df = final_df.copy()
        flagged_df["anti_india_flag"] = flagged_df["anti_india_keyword"].apply(lambda x: eval(str(x))[0])
        flagged_df = flagged_df[flagged_df["anti_india_flag"] == True]

        if not flagged_df.empty:
            st.markdown("### ⚠️ Flagged Anti-India Posts")
            st.caption("These posts are detected as Anti-India. Quick action recommended.")

            # Select only key columns for display
            display_cols = ["username", "link", "translated_text","sentiment", "anti_india_flag", "bot_label"]
            show_df = flagged_df[display_cols].copy()

            # Fill NaN links with placeholder
            show_df["link"] = show_df["link"].fillna("")


            # Show scrollable dataframe with clickable link column
            st.dataframe(
               show_df,
               use_container_width=True,
               height=400,
               column_config={
                  "link": st.column_config.LinkColumn("link", display_text="🔗 Go to Post")
               }
            )


            # Download full flagged dataset
            csv_data = flagged_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Anti-India Report",
                data=csv_data,
                file_name="anti_india_flagged.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ No Anti-India posts detected in this dataset.")


# Footer with pipeline information
st.divider()
st.markdown("""
### 🔄 Pipeline Information
This dashboard orchestrates the complete data processing workflow for the ANTI_INDIA_GUARD project:

1. **Fetch Twitter Data** → Raw tweet collection
2. **Generate Dummy Tweets** → Data augmentation  
3. **Translate Text** → Language normalization
4. **Clean Text** → Data preprocessing
5. **Sentiment Analysis** → Emotional analysis
6. **Bot Detection** → Account authenticity check

Each step generates a CSV file that feeds into the next stage of the pipeline.
""")
