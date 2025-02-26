import streamlit as st
import pandas as pd
import requests

# Streamlit app title
st.title("Spotify Data Filter")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data:")
    st.dataframe(df.head())

    # Check if necessary columns exist
    required_columns = {"danceability", "genre", "artist"}
    if not required_columns.issubset(df.columns):
        st.error(f"CSV file must contain the following columns: {required_columns}")
    else:
        with st.sidebar:
            st.header("Filter Options")
            min_danceability, max_danceability = st.slider(
                "Select Danceability Range",
                min_value=float(df["danceability"].min()),
                max_value=float(df["danceability"].max()),
                value=(float(df["danceability"].min()), float(df["danceability"].max())),
                step=0.01
            )
            genre = st.selectbox("Select Genre", ["All"] + sorted(df["genre"].dropna().unique()))
            artist = st.selectbox("Select Artist", ["All"] + sorted(df["artist"].dropna().unique()))

        # Apply filters
        filtered_df = df[
            (df["danceability"] >= min_danceability) & (df["danceability"] <= max_danceability)
        ]
        if genre != "All":
            filtered_df = filtered_df[filtered_df["genre"].str.contains(genre, case=False, na=False)]
        if artist != "All":
            filtered_df = filtered_df[filtered_df["artist"].str.contains(artist, case=False, na=False)]

        st.write("### Filtered Data:")
        st.dataframe(filtered_df)


FASTAPI_URL = "http://127.0.0.1:8000"

def call_fastapi(song_data):
    try:
        response = requests.post(f"{FASTAPI_URL}/predict", json=song_data)
        response.raise_for_status()
        data = response.json()
        if "results" in data:
            st.write("### Prediction Results:")
            st.dataframe(pd.DataFrame(data["results"]))
        else:
            st.warning("Unexpected API response format.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with FastAPI: {e}")

if st.button("Predict"):
    if uploaded_file is not None:
        song_data = df.to_dict(orient="records")
        call_fastapi(song_data)
    else:
        st.error("Please upload a file first.")
s