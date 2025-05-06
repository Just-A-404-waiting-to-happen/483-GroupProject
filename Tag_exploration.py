import pandas as pd

# Load the CSV file
df = pd.read_csv('E:/song_lyrics.csv')

# Get all unique tags (case-sensitive)
unique_tags = df['tag'].unique()

# Print all unique tags
print("All unique tags in the dataset:")
for tag in sorted(unique_tags):
    print(f"- {tag}")

# Count of unique tags
print(f"\nTotal unique tags found: {len(unique_tags)}")
