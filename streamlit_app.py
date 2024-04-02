import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import datetime
from matplotlib.ticker import FuncFormatter

st.sidebar.header('Spotify Data Analysis')
uploaded_file = st.sidebar.file_uploader("Choose a ZIP file", type="zip")
analysis_type = st.sidebar.selectbox(
    "Choose the type of analysis",
    ("Top 10 Albums of 2023", "Top 5 Listened to Artists of All Time")
)

if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, 'r') as zf:
        dfs = []
        for name in zf.namelist():
            if 'Streaming_History_Audio_' in name:
                dfs.append(pd.read_json(zf.open(name)))
        df = pd.concat(dfs)
        df['ts'] = pd.to_datetime(df['ts'])


if analysis_type == "Top 10 Albums of 2023" and df is not None:
    df_album_by_year = df[df['ts'].dt.year == 2023]
    df_album_by_year = df_album_by_year.groupby(['master_metadata_album_album_name', 'master_metadata_album_artist_name'])['ms_played'].sum().sort_values(ascending=False)[:10]
    albums = [f"{album} - {artist}" for (album, artist) in df_album_by_year.index.values]
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.barh(albums, df_album_by_year)
    ax.set_title('Top albums of 2023')
    ax.invert_yaxis()
    st.pyplot(fig)     