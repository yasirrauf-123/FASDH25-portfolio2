"""
This script is written as a part of our Digital Humanities course Mini Project No.2
where we explore how to visualize the places that are mentioned in news articles
over time.
We are using computational tools to find toponyms (= place names) in each article,
put them on a map, and visualize how the geographic scope of the news articles
shifts over time.
In this script we are using regular expressions and a gazetter to extract place names
from a collection of news articles about the war in Gaza, collected from the Aljzeera
English website by Inacio Vieira. The full collection contains 4341 different articles,
and although the title of the dataset suggests that the dataset covers the Gaza War
since November 2023, the dataset also contains earlier articles but in the script we are
using a condition to skips the articles that were written before the start of the
current war because we want to only work with the articles after the war to visualize how
the geographic scope of the news articles have shifted after war in Gaza started.
"""
# Importing regex libary to find place names in the text using the regular expressions
import re
# Importing os to interact with the operating system (files and directorie we want to work with)
import os
# Importing pandas as pd to save our results in a structured table format (tsv)
import pandas as pd

# Set the paths to the gazetteer and articles folder
gazetteer_path = "../gazetteers/geonames_gaza_selection.tsv"  # Path to the gazetteer file
articles_folder = "../articles"  # Path to the folder containing news articles

# Reading the gazetteer file which contains place names to extract from articles
with open(gazetteer_path, encoding="utf-8") as file:
    data = file.read()  # Read the entire gazetteer file content

# code below this upto patterns[ascii_name] = all_names have been generated with the help of ChatGPT(ChatGPT Solution 1 in AI Documentation)
# Creating a dictionary to store place name patterns for regex matching
patterns = {}

# Split the gazetteer data into rows (one for each place name)
rows = data.strip().split("\n")

# The first row usually contains column names: ascii, name, alternate names
header = rows[0].split("\t")

# Process each row to extract the place names and alternate names
for row in rows[1:]:
    columns = row.split("\t")
    
    # Skip rows with missing information
    if len(columns) < 3:
        continue

    # Extract and clean up place names
    ascii_name = columns[0].strip()  # Simple version of the place name
    name = columns[1].strip()  # Full or official name of the place
    alt_names = columns[2].strip()  # Alternate names as a comma-separated string

    # Create a list of all names (official and alternate) for the place
    alt_names_list = [alt.strip() for alt in alt_names.split(",") if alt.strip()]
    all_names = [ascii_name, name] + alt_names_list

    # Store the list of names in the dictionary using the ascii_name as the key
    patterns[ascii_name] = all_names

# code below this upto pattern_to_place[regex] = ascii_name has been generated with the help of ChatGPT see ChatGPT solution No.3 in AI documentation
# Create regex patterns to search for each place name using the list of names
pattern_to_place = {}

# For each place in the patterns dictionary, create a regex pattern to match all its names
for ascii_name, name_list in patterns.items():
    # Combine the names into a single regex pattern (separated by "|")
    regex = "|".join(re.escape(name) for name in name_list if name)
    pattern_to_place[regex] = ascii_name

# Creating a dictionary named frequency_counter to count total mentions of each place name
frequency_counter = {}

# Creating a dictionary named mentions_per_month to count mentions of places per months
mentions_per_month = {}

# Processing each article to count mentions of places
for filename in os.listdir(articles_folder):
    # Extract the date and month from the filename
    file_date = filename[:10]  # Extract date like '2023-11-05'
    file_month = file_date[:7]  # Extract month like '2023-11'

    # Skip articles before the war started on 2023-10-07
    if file_date < "2023-10-07":
        continue

    # Open and read the article's content
    file_path = os.path.join(articles_folder, filename)
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    # code generated with the help of ChatGPT see ChatGPT solution No.4 in AI Documentation
    # Set to keep track of places already counted in the current article
    already_counted_places = set()

    # Search for each place name using the regex patterns
    for regex, place in pattern_to_place.items():
        # Skip if the place has already been counted in this article
        if place in already_counted_places:
            continue

        # Use regex to find all occurrences of the place name in the article
        matches = re.findall(rf"\b(?:{regex})\b", text, flags=re.IGNORECASE)
        count = len(matches)  # Count how many times the place appears

        # If the place was mentioned, update the total and monthly counts
        if count > 0:
            # Update total frequency count for the place
            frequency_counter[place] = frequency_counter.get(place, 0) + count

            # Update mentions by month for the place
            if place not in mentions_per_month:
                mentions_per_month[place] = {}

            mentions_per_month[place][file_month] = mentions_per_month[place].get(file_month, 0) + count

            # Mark this place as counted in the current article
            already_counted_places.add(place)

# code generated with the help of ChatGPT see ChatGPT solution No.2 and ChatGPT Solution No.6 in AI documentation
# Output the frequency counts for each place and its monthly mentions
for place in frequency_counter:
    total = frequency_counter[place]

    # Print the total frequency count for the place if it's mentioned at least once
    if total > 0:
        print(f"Found {place} {total} times")

        # Print the frequency count for each month the place was mentioned
        for month, count in mentions_per_month.get(place, {}).items():
            if count > 0:
                print(f"  Found {place} {count} times in {month}")
# Code below have been generated with the help of chatGPT (see ChatGPT Solution No.7 in AI Documentation)
# Create an empty list to store the rows we want to save
# Each row will be a tuple: (placename, month, count)
rows_to_write = []

# Loop through each place and its monthly data in the mentions_per_month dictionary
for place, month_data in mentions_per_month.items():
    
    # For each place, loop through its months and the corresponding count of mentions
    for month, count in month_data.items():
        
        # Only include data where the mention count is greater than zero
        # This filters out months where a place wasn't mentioned
        if count > 0:
            # Add a tuple with the place name, month, and count to the list
            rows_to_write.append((place, month, count))

# Convert the list of rows (tuples) into a pandas DataFrame (like a table)
# The DataFrame will have three columns: placename, month, and count
df = pd.DataFrame(rows_to_write, columns=["placename", "month", "count"])

# Save the DataFrame as a .tsv (tab-separated values) file
# sep="\t" means values will be separated by tabs
# index=False means we don't want to write row numbers to the file
df.to_csv("regex_counts.tsv", sep="\t", index=False)
