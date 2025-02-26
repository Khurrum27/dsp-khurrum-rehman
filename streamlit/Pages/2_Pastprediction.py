import streamlit as st
import pandas as pd
import requests

st.title("📊 Past Predictions")

FASTAPI_URL = "http://127.0.0.1:8000/results"

# Date selection
start_date = st.date_input("📅 Select Start Date")
end_date = st.date_input("📅 Select End Date")

# Prediction source selection
prediction_source = st.selectbox("🔍 Select Prediction Source", ["All", "WebApp", "Scheduled Predictions"])

# Fetch data from FastAPI
def fetch_past_predictions():
    try:
        response = requests.get(FASTAPI_URL)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data["results"]) if "results" in data else pd.DataFrame()

        # Ensure "created_at" column exists
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"])
        else:
            st.warning("⚠️ 'created_at' column is missing from API response.")
            df["created_at"] = pd.to_datetime("today")  # Default value

        return df

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching data: {e}")
        return pd.DataFrame()

df = fetch_past_predictions()

if not df.empty:
    df_filtered = df.copy()


    if "created_at" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["created_at"] >= pd.to_datetime(start_date)) &
            (df_filtered["created_at"] <= pd.to_datetime(end_date))
        ]

    # Apply source filter
    if prediction_source != "All":
        df_filtered = df_filtered[df_filtered["source"] == prediction_source]

    st.write("### 📊 Filtered Predictions")
    st.dataframe(df_filtered)

else:
    st.warning("⚠️ No data available. Try selecting different filters.")
    