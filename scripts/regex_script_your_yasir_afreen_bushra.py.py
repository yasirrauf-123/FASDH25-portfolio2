"""
This is the final version of the regex script for our Digital Humanities Mini-Project 2.

The script does the following:
- Loads a gazetteer of place names with multiple spelling variants.
- Reads through many news article files about the Gaza war.
- Finds how often each place name is mentioned in the text of these articles.
- Only includes articles that were written during the current war (after October 2023).
- Counts how often each place is mentioned each month.
- Saves this information in a TSV file called "regex_counts.tsv".

"""

import re         # for finding place names in text using patterns (regex)
import os         # for reading all the files in the articles folder
import pandas as pd  # to save our results in a structured table format

# Set the paths to the gazetteer and the articles folder
gazetteer_path = "../gazetteers/geonames_gaza_selection.tsv"
articles_folder = "../articles"

# Load the gazetteer
with open(gazetteer_path, encoding="utf-8") as file:
    data = file.read()

# Create two dictionaries:
# 1. frequency_counter to count total mentions of each place name
# 2. mentions_per_month to count mentions per month
frequency_counter = {}
mentions_per_month = {}

# Extract all names for each place from the gazetteer
rows = data.strip().split("\n")
header = rows[0].split("\t")  # column names
rows = rows[1:]  # skip header

# This will store regex patterns as keys and place names as values
pattern_to_place = {}

for row in rows:
    columns = row.split("\t")
    asciiname = columns[0]
    alternatenames = columns[3] if len(columns) > 3 else ""  # Get alternative names if available

    # Combine the asciiname and alternate names
    all_names = [asciiname] + alternatenames.split(",")

    # Remove duplicates and empty strings
    all_names = list(set([name.strip() for name in all_names if name.strip()]))

    # Build a simple regex that matches any of these names using '|'
    # Note: this is a basic method to improve recall
    regex_pattern = "|".join(re.escape(name) for name in all_names)

    # Save the regex and the asciiname (we'll use asciiname as the display name)
    pattern_to_place[regex_pattern] = asciiname

    # Initialize the counters
    frequency_counter[asciiname] = 0
    mentions_per_month[asciiname] = {}

# Go through all the article files
for filename in os.listdir(articles_folder):

    
    # Get the date from the filename (format: 2023-11-05_xyz.txt → "2023-11")
    file_date = filename[:10]  # YYYY-MM-DD
    file_month = file_date[:7]  # YYYY-MM

    # Skip files from before the current war (before 2023-10-07)
    if file_date < "2023-10-07":
        continue

    # Open and read the file
    file_path = os.path.join(articles_folder, filename)
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    # Step 4: Search for place names using all the regex patterns
    for regex, place in pattern_to_place.items():
        matches = re.findall(rf"\b(?:{regex})\b", text, flags=re.IGNORECASE)
        count = len(matches)

        # Update total frequency
        frequency_counter[place] += count

        # Update monthly frequency
        if file_month not in mentions_per_month[place]:
            mentions_per_month[place][file_month] = 0
        mentions_per_month[place][file_month] += count


# Print the total count and monthly breakdown of each place
for place in mentions_per_month:
    print("found", place, "times in total:", sum(mentions_per_month[place].values()))

    # Print how many times it was mentioned in each month
    for month in mentions_per_month[place]:
        print("   in", month, ":", mentions_per_month[place][month], "times")

# Write results to a TSV file called "regex_counts.tsv"
# This file will have 3 columns: placename, month, count
rows_to_write = []

for place, month_data in mentions_per_month.items():
    for month, count in month_data.items():
        if count > 0:
            rows_to_write.append((place, month, count))

# Convert to DataFrame and save
df = pd.DataFrame(rows_to_write, columns=["placename", "month", "count"])
df.to_csv("regex_counts.tsv", sep="\t", index=False)




