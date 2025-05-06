import pandas as pd

# Load the CSV file
df = pd.read_csv('E:/song_lyrics.csv')

# Filter English songs and select needed columns
english_songs = df.query("language == 'en'")[['artist', 'title', 'tag', 'lyrics']]

# Clean and standardize tags (convert to lowercase and strip whitespace)
english_songs['tag'] = english_songs['tag'].str.lower().str.strip()

# Define the 6 specific tags we want
tags = ['country', 'misc', 'pop', 'rap', 'rb', 'rock']

# Process each tag
for tag in tags:
    # Filter songs for this tag (exact match)
    tag_songs = english_songs[english_songs['tag'] == tag]

    if not tag_songs.empty:
        # Create filename with the tag name
        filename = f'songs_{tag}.csv'

        # Save to CSV
        tag_songs.to_csv(filename, index=False)
        print(f"Saved {len(tag_songs)} {tag} songs to {filename}")
    else:
        print(f"No songs found for tag: {tag}")


other_songs = english_songs[~english_songs['tag'].isin(tags)]
if not other_songs.empty:
    other_songs.to_csv('songs_other_tags.csv', index=False)
    print(f"Saved {len(other_songs)} songs with other tags to songs_other_tags.csv")