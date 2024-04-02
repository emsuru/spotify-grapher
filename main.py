# this script works for the sample data you get from Spotify in a zip file (will update soon for full dataset)

import datetime
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.ticker import FuncFormatter

# Initialize an empty list to store individual dataframes
dfs = []
# Open the zip file containing Spotify data in read mode
zf = zipfile.ZipFile('my_spotify_data.zip', 'r')
# Iterate through each file name in the zip file
for name in zf.namelist():
    # Skip files that do not contain 'StreamingHistory' in their name
    if 'StreamingHistory' not in name:
        continue
    # Read the JSON file into a pandas dataframe and append it to the list of dataframes
    dfs.append(pd.read_json(zf.open(name)))

# Concatenate all dataframes in the list into a single dataframe
df = pd.concat(dfs)

print("Columns:", df.columns.values)
print("Number of streams:", str(df.shape[0]))
#print(datetime.timedelta(milliseconds=int(df['ms_played'].sum())))
def format_ms(x, pos):
    return str(round(x/(3.6e+6), 2)) + 'h'

# Filter by year, group by artist, sum time played and take top ten.
year_df = df.loc[pd.to_datetime(df['endTime']).apply(lambda t: t.year == 2023)]
year_df = year_df.groupby(['trackName'])[['msPlayed']].sum()
year_df = year_df.sort_values('msPlayed', ascending=False)
year_df = year_df[:10]

fig, ax = plt.subplots()

plt.gca().xaxis.set_major_formatter(format_ms)
ax.barh(year_df.index.values, year_df['msPlayed'])
ax.set_title('Top 10 songs (Jan 2023 - Feb 2024)')
ax.invert_yaxis()
plt.savefig('top_10_songs.png', dpi=300, bbox_inches='tight')
plt.show()


# Determine top artists listened to.
top_artists_df = df.groupby(['artistName'])[['msPlayed']]
top_artists_df = top_artists_df.sum().sort_values('msPlayed', ascending=False)[:5]
top_artists = [artist for (artist) in top_artists_df.index.values]

fig, ax = plt.subplots(figsize=(10, 5))
for artist in top_artists:
  # Generate rolling sums of total amount of time listening to the artist.
  df2 = df.loc[df['artistName'] == artist][['endTime', 'msPlayed']]
  df2['endTime'] = df2['endTime'].apply(pd.to_datetime)
  df2 = df2.sort_values('endTime')
  df2 = df2.rolling('365D', on='endTime').sum()
  ax.plot(df2['endTime'], df2['msPlayed'], label=artist)

ax.set_title('Top 5 artists (Jan 2023 - Feb 2024)')
plt.gca().yaxis.set_major_formatter(format_ms)
plt.legend()
plt.savefig('top_5_artists.png', dpi=300, bbox_inches='tight')
plt.show()
