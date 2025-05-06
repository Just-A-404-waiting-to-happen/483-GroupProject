import pandas as pd

# Load the CSV file
df = pd.read_csv('E:/song_lyrics.csv')
# filtering the data down to english songs: artist, title, tag, lyrics. as the other data is unnessiary for this project.
english_songs = df.query("language == 'en'")[['artist', 'title', 'tag', 'lyrics']]

english_songs.to_csv('songs_filtered.csv', index=False)
