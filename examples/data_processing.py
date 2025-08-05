"""
Core data processing utilities extracted from the Spotify Grapher project.
These functions demonstrate the essential patterns for processing Spotify streaming data.
"""

import pandas as pd
import zipfile
from typing import List, Dict, Any
import datetime


def load_spotify_data_from_zip(zip_path: str, file_pattern: str = 'StreamingHistory') -> pd.DataFrame:
    """
    Load Spotify streaming data from a zip file.
    
    Args:
        zip_path: Path to the Spotify data zip file
        file_pattern: Pattern to match JSON files (e.g., 'StreamingHistory' or 'Streaming_History_Audio_')
    
    Returns:
        Concatenated DataFrame of all matching JSON files
    """
    dfs = []
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for name in zf.namelist():
            if file_pattern in name:
                dfs.append(pd.read_json(zf.open(name)))
    
    return pd.concat(dfs) if dfs else pd.DataFrame()


def calculate_top_tracks(df: pd.DataFrame, year: int = None, limit: int = 10) -> pd.DataFrame:
    """
    Calculate top tracks by total listening time.
    
    Args:
        df: DataFrame with Spotify streaming data
        year: Optional year filter
        limit: Number of top tracks to return
    
    Returns:
        DataFrame with top tracks sorted by play time
    """
    result_df = df.copy()
    
    # Filter by year if specified
    if year and 'endTime' in df.columns:
        result_df = df.loc[pd.to_datetime(df['endTime']).apply(lambda t: t.year == year)]
    elif year and 'ts' in df.columns:
        result_df = df.loc[pd.to_datetime(df['ts']).apply(lambda t: t.year == year)]
    
    # Group by track name and sum play time
    if 'trackName' in result_df.columns:
        result_df = result_df.groupby(['trackName'])[['msPlayed']].sum()
    elif 'master_metadata_track_name' in result_df.columns:
        result_df = result_df.groupby(['master_metadata_track_name'])[['ms_played']].sum()
        result_df.columns = ['msPlayed']
    
    return result_df.sort_values('msPlayed', ascending=False).head(limit)


def calculate_top_artists(df: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    """
    Calculate top artists by total listening time.
    
    Args:
        df: DataFrame with Spotify streaming data
        limit: Number of top artists to return
    
    Returns:
        DataFrame with top artists sorted by play time
    """
    # Handle different column naming conventions
    if 'artistName' in df.columns:
        artist_col = 'artistName'
        time_col = 'msPlayed'
    else:
        artist_col = 'master_metadata_album_artist_name'
        time_col = 'ms_played'
    
    top_artists_df = df.groupby([artist_col])[[time_col]].sum()
    return top_artists_df.sort_values(time_col, ascending=False).head(limit)


def calculate_rolling_artist_history(df: pd.DataFrame, artist: str, window: str = '365D') -> pd.DataFrame:
    """
    Calculate rolling sum of listening time for a specific artist.
    
    Args:
        df: DataFrame with Spotify streaming data
        artist: Artist name to analyze
        window: Rolling window size (default: 365 days)
    
    Returns:
        DataFrame with timestamp and rolling sum of play time
    """
    # Handle different column naming conventions
    if 'artistName' in df.columns:
        artist_col = 'artistName'
        time_col = 'endTime'
        play_col = 'msPlayed'
    else:
        artist_col = 'master_metadata_album_artist_name'
        time_col = 'ts'
        play_col = 'ms_played'
    
    artist_df = df.loc[df[artist_col] == artist][[time_col, play_col]]
    artist_df[time_col] = pd.to_datetime(artist_df[time_col])
    artist_df = artist_df.sort_values(time_col)
    artist_df = artist_df.rolling(window, on=time_col).sum()
    
    return artist_df


def format_milliseconds_to_hours(ms: int) -> str:
    """
    Convert milliseconds to a human-readable hours format.
    
    Args:
        ms: Time in milliseconds
    
    Returns:
        Formatted string with hours
    """
    hours = ms / 3.6e+6
    return f"{hours:.2f}h"


def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get a summary of the Spotify data.
    
    Args:
        df: DataFrame with Spotify streaming data
    
    Returns:
        Dictionary with summary statistics
    """
    # Handle different column naming conventions
    time_col = 'msPlayed' if 'msPlayed' in df.columns else 'ms_played'
    
    total_ms = df[time_col].sum()
    total_time = datetime.timedelta(milliseconds=int(total_ms))
    
    return {
        'total_streams': len(df),
        'total_listening_time_ms': total_ms,
        'total_listening_time': str(total_time),
        'unique_tracks': df.get('trackName', df.get('master_metadata_track_name', [])).nunique(),
        'unique_artists': df.get('artistName', df.get('master_metadata_album_artist_name', [])).nunique(),
        'columns': list(df.columns),
    }