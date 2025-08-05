# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python data visualization project for analyzing Spotify streaming history. It processes JSON data from Spotify's data export and generates visualizations of listening patterns.

## Key Commands

### Running the main analysis script
```bash
python main.py
```
This generates two visualization files: `top_10_songs.png` and `top_5_artists.png` from `my_spotify_data.zip`.

### Running the Streamlit web app
```bash
streamlit run streamlit_app.py
```
Launches an interactive web interface for uploading and analyzing Spotify data.

### Installing dependencies
```bash
pip install -r requirements.txt
```

## Architecture Overview

The codebase has two main entry points:

1. **main.py**: Standalone script that processes `my_spotify_data.zip` directly
   - Reads JSON files containing StreamingHistory from the zip
   - Groups data by track/artist and calculates total listening time
   - Generates static matplotlib charts saved as PNG files

2. **streamlit_app.py**: Interactive web application
   - Allows users to upload their Spotify data zip file
   - Processes files containing "Streaming_History_Audio_" prefix (full export format)
   - Provides dynamic analysis options through sidebar controls

## Data Processing Pattern

Both scripts follow a similar data processing flow:
1. Extract JSON files from zip archive
2. Concatenate multiple JSON files into a single pandas DataFrame
3. Parse timestamps and calculate time aggregations (ms_played)
4. Group by relevant dimensions (artist, track, album)
5. Generate visualizations using matplotlib

The notebook `AskTheData.ipynb` contains exploratory analysis and additional visualizations for the full Spotify data export format which includes more detailed metadata fields.

## Important Notes

- The project handles two different Spotify data export formats:
  - Sample data: Contains files with "StreamingHistory" prefix (used in main.py)
  - Full export: Contains files with "Streaming_History_Audio_" prefix (used in streamlit_app.py and notebook)
- Time calculations use milliseconds (ms_played field) converted to hours for display
- Visualizations use matplotlib with custom formatters for time display