"""
Visualization utilities for creating engaging charts from Spotify data.
These functions demonstrate different ways to visualize listening patterns.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import pandas as pd
from typing import List, Optional, Tuple, Any


def create_horizontal_bar_chart(
    data: pd.Series,
    title: str,
    x_formatter: Optional[FuncFormatter] = None,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> Tuple[Any, Any]:
    """
    Create a horizontal bar chart for top items.
    
    Args:
        data: Series with index as labels and values as quantities
        title: Chart title
        x_formatter: Optional formatter for x-axis values
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
    
    Returns:
        Tuple of (figure, axis) objects
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if x_formatter:
        ax.xaxis.set_major_formatter(x_formatter)
    
    ax.barh(data.index.values, data.values)
    ax.set_title(title)
    ax.invert_yaxis()  # Top items at the top
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def create_time_series_plot(
    data_dict: dict,
    title: str,
    y_formatter: Optional[FuncFormatter] = None,
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None
) -> Tuple[Any, Any]:
    """
    Create a time series plot for multiple artists/items over time.
    
    Args:
        data_dict: Dictionary with labels as keys and DataFrames with 'time' and 'value' columns
        title: Chart title
        y_formatter: Optional formatter for y-axis values
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
    
    Returns:
        Tuple of (figure, axis) objects
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for label, df in data_dict.items():
        ax.plot(df.iloc[:, 0], df.iloc[:, 1], label=label)
    
    ax.set_title(title)
    
    if y_formatter:
        ax.yaxis.set_major_formatter(y_formatter)
    
    plt.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def create_milliseconds_formatter() -> FuncFormatter:
    """
    Create a formatter that converts milliseconds to hours.
    
    Returns:
        FuncFormatter for matplotlib axes
    """
    def format_ms(x, pos):
        return f'{x/3.6e+6:.1f}h'
    
    return FuncFormatter(format_ms)


def create_timedelta_formatter() -> FuncFormatter:
    """
    Create a formatter that converts milliseconds to timedelta format.
    
    Returns:
        FuncFormatter for matplotlib axes
    """
    import datetime
    
    def format_ms_timedelta(x, pos):
        td = datetime.timedelta(milliseconds=x)
        days = td.days
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        
        if days > 0:
            return f'{days}d {hours}h'
        elif hours > 0:
            return f'{hours}h {minutes}m'
        else:
            return f'{minutes}m'
    
    return FuncFormatter(format_ms_timedelta)


def create_listening_pattern_heatmap(
    df: pd.DataFrame,
    time_col: str = 'ts',
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None
) -> Tuple[Any, Any]:
    """
    Create a heatmap showing listening patterns by hour and day of week.
    
    Args:
        df: DataFrame with timestamp column
        time_col: Name of the timestamp column
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
    
    Returns:
        Tuple of (figure, axis) objects
    """
    import numpy as np
    
    # Convert to datetime if needed
    df[time_col] = pd.to_datetime(df[time_col])
    
    # Extract hour and day of week
    df['hour'] = df[time_col].dt.hour
    df['day_of_week'] = df[time_col].dt.dayofweek
    
    # Create pivot table for heatmap
    heatmap_data = df.pivot_table(
        index='hour',
        columns='day_of_week',
        values=time_col,
        aggfunc='count',
        fill_value=0
    )
    
    # Create the heatmap
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.imshow(heatmap_data.T, cmap='YlOrRd', aspect='auto')
    
    # Set ticks and labels
    ax.set_xticks(np.arange(24))
    ax.set_yticks(np.arange(7))
    ax.set_xticklabels([f'{i:02d}:00' for i in range(24)])
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    
    # Rotate the tick labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add colorbar
    plt.colorbar(im, ax=ax, label='Number of streams')
    
    ax.set_title('Listening Pattern Heatmap')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Day of Week')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax


def create_genre_diversity_plot(
    df: pd.DataFrame,
    artist_col: str = 'master_metadata_album_artist_name',
    time_col: str = 'ms_played',
    top_n: int = 20,
    figsize: Tuple[int, int] = (10, 10),
    save_path: Optional[str] = None
) -> Tuple[Any, Any]:
    """
    Create a pie chart showing diversity of listening across artists.
    
    Args:
        df: DataFrame with artist and play time columns
        artist_col: Name of the artist column
        time_col: Name of the play time column
        top_n: Number of top artists to show individually (others grouped)
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
    
    Returns:
        Tuple of (figure, axis) objects
    """
    # Calculate top artists
    artist_stats = df.groupby(artist_col)[time_col].sum().sort_values(ascending=False)
    
    # Separate top N and others
    top_artists = artist_stats.head(top_n)
    others_sum = artist_stats.iloc[top_n:].sum()
    
    if others_sum > 0:
        top_artists = pd.concat([
            top_artists,
            pd.Series([others_sum], index=['Others'])
        ])
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = plt.cm.Set3(range(len(top_artists)))
    
    wedges, texts, autotexts = ax.pie(
        top_artists.values,
        labels=top_artists.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    
    # Improve text readability
    for text in texts:
        text.set_fontsize(8)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(7)
        autotext.set_weight('bold')
    
    ax.set_title(f'Listening Diversity (Top {top_n} Artists)')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax