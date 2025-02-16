import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Spotify Data Filter")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data:")
    st.dataframe(df.head())
    
    # Check if necessary columns exist
    required_columns = {"danceability", "genre", "artist"}  
    if not required_columns.issubset(df.columns):
        st.error(f"CSV file must contain the following columns: {required_columns}")
    else:
        # Sidebar for interactive filters
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
        
        # Apply filters dynamically
        filtered_df = df[
            (df["danceability"] >= min_danceability) & (df["danceability"] <= max_danceability)
        ]
        
        if genre != "All":
            filtered_df = filtered_df[filtered_df["genre"].str.contains(genre, case=False, na=False)]
        
        if artist != "All":
            filtered_df = filtered_df[filtered_df["artist"].str.contains(artist, case=False, na=False)]
        
        st.write("### Filtered Data:")
        st.dataframe(filtered_df)

        # Display Predict Button at Bottom Right
        st.markdown(
            """
            <style>
            .predict-container {
                display: flex;
                justify-content: flex-end;
                padding: 20px;
            }
            .predict-button {
                background-color: #4CAF50; /* Green */
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            }
            .predict-button:hover {
                background-color: #45a049; /* Darker Green */
            }
            </style>
            <div class="predict-container">
                <button class="predict-button" onclick="window.location.reload();">🔮 Predict</button>
            </div>
            """,
            unsafe_allow_html=True
        )
