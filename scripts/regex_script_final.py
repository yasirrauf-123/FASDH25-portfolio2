"""
This script is part of our Digital Humanities course Mini Project No. 2, where we explore how to visualize
the places mentioned in news articles over time. Using computational tools, we extract toponyms (place names)
from each article, map them, and observe how the geographic focus of the news shifts. In this script, we apply regular
expressions and a gazetteer to a dataset of 4341 Al Jazeera English articles about the Gaza war, collected by
Inacio Vieira. Although the dataset includes older articles, we use a condition to skip those published before
the current war (starting November 2023), as our focus is on mapping how the geographic focus of news articles has shifted
since the start of the ongoing conflict in Gaza.
"""

# Importing the regex library to extract place names from text using regular expressions
import re
# Importing os to interact with the operating system (e.g., accessing files and directories)
import os
# Importing pandas as pd to store our results in a structured table format (TSV)
import pandas as pd

# Setting the path to the gazetteer file, which contains place names we want to match
gazetteer_path = "../gazetteers/geonames_gaza_selection.tsv"

# Setting the path to the folder containing the news articles to be processed
articles_folder = "../articles"

# Opening the gazetteer file that contains place names we want to extract from the articles
with open(gazetteer_path, encoding="utf-8") as file:
    data = file.read()  # Reading the entire content of the gazetteer file

# Code from below up to line 66 has been fixed with the help of ChatGPT (ChatGPT Solution No.1 in AI Documentation Document)
# Creating Dictionary to store regex patterns for each place (keyed by ascii name)
patterns = {}
# Split the gazetteer file into rows using newline as the separator
rows = data.split("\n")
# Extract column indices from the header row to correctly access columns by name
header = rows[0].split("\t")
# Get index of the 'ascii' column 
ascii_idx = header.index("asciiname")
# Get index of the 'name' column
name_idx = header.index("name")
# Get index of the 'alternate names' column
alt_names_idx = header.index("alternatenames")
# Loop through all rows except the header 
for row in rows[1:]: 
    cells = row.split("\t")  # Split the row into individual cell values by tab     
    # Skip the row if it's incomplete (e.g., missing required columns) 
    if len(cells) <= max(ascii_idx, name_idx, alt_names_idx): 
        continue
    # Extract and clean up the values for each relevant column 
    ascii_name = cells[ascii_idx].strip()  # Primary name (used as dictionary key) 
    name = cells[name_idx].strip()         # Official or canonical name 
    alt_names = cells[alt_names_idx].strip()  # Comma-separated alternate name
    # Split alternate names into a list, trimming spaces; fallback to empty list if blank 
    alt_list = [n.strip() for n in alt_names.split(",")] if alt_names else [] 
 
    # Combine all name variants into a set to remove duplicates 
    name_variants = set([ascii_name, name] + alt_list) 
 
    # Escape each name to safely include in regex (e.g., handles special characters like "." or "+") 
    escaped_names = [re.escape(n) for n in name_variants if n] 
 
    # Only proceed if there's at least one name to include 
    if escaped_names: 
        # Create a regex pattern that matches any of the name variants as whole words 
        # \b ensures we only match complete words (not substrings) 
        pattern = r"\b(?:{})\b".format("|".join(escaped_names)) 
 
        # Compile the pattern with case-insensitive matching for flexibility in text 
        patterns[ascii_name] = re.compile(pattern, re.IGNORECASE)

# Creating a dictionary named frequency_counter to track the total mentions of each place name
frequency_counter = {}

# Creating a dictionary named mentions_per_month to track place name mentions by month
mentions_per_month = {}

# Code from below up to line 118 has been fixed with the help of ChatGPT (see ChatGPT Solution No.2 in AI documentation)
# Looping through each article to count place name mentions
for filename in os.listdir(articles_folder):
    # Extracting the date and month from the filename 
    file_date = filename[:10]  
    file_month = file_date[:7]

    # Skipping articles published before the Gaza war began (2023-10-07)
    if file_date < "2023-10-07":
        continue

    # Opening and reading the content of the article
    file_path = os.path.join(articles_folder, filename)
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    # Reset counted places for each new article
    # Code below have been fixed with the help of ChatGPT (see ChatGPT solution No.4 in AI documentation)
    already_counted_places = set()

    # Loop through each compiled regex pattern and its corresponding place name
    # Code below have been fixed with the help of ChatGPT (see ChatGPT Solution No.3 in AI documentation)
    for place, regex in patterns.items():

        # We only want to count each place **once per article**, 
        # so if we've already counted this place in the current article, we skip it
        if place in already_counted_places:
            continue

        # Use compiled regex to find all case-insensitive matches of the place name in the article's text
        # Code below have been fixed with the helped with the help of ChatGPT (See ChatGPT Solution No.5 in AI documentation)
        matches = regex.findall(text)

        # Count how many times the place name appears in the article
        count = len(matches)

        # If the place was mentioned at least once in the article
        if count > 0:

            # Update the total count of how many times this place has been mentioned across all articles
            frequency_counter[place] = frequency_counter.get(place, 0) + count

            # If this is the first time the place is being added to the monthly dictionary, initialize it
            if place not in mentions_per_month:
                mentions_per_month[place] = {}

            # Update the count of mentions for this place in the current month
            mentions_per_month[place][file_month] = mentions_per_month[place].get(file_month, 0) + count

            # Mark this place as already counted for this article so it's not double-counted
            already_counted_places.add(place)

# Printing the frequency counts for each place and its monthly mentions to check whether our run whether our script has ran properly
# Code below was self written and then was fixed with the help of ChatGPT (See ChatGPT Solution No.6)
for place in frequency_counter:
    total = frequency_counter[place]

    # Print the total frequency count for the place if it's mentioned at least once
    if total > 0:
        print(f"Found {place} {total} times")

        # Print the frequency count for each month the place was mentioned
        for month, count in mentions_per_month.get(place, {}).items():
            if count > 0:
                print(f"  Found {place} {count} times in {month}")

# Create an empty list to store the rows we want to save
# Code below have been written and fixed with the help of ChatGPT (see ChatGPT Solution No.7 in AI Documentation)
# Each row will be a tuple: (placename, month, count)
rows_to_write = []

# Loop through each place and its monthly data in the mentions_per_month dictionary
for place, month_data in mentions_per_month.items():
    
    # For each place, loop through its months and the corresponding count of mentions
    for month, count in month_data.items():
        
        # Only include data where the mention count is greater than zero
        # This filters out months where a place wasn't mentioned- we are doing this for sanity check
        if count > 0:
            # Add a tuple with the place name, month, and count to the list
            rows_to_write.append((place, month, count))

# Convert the list of rows (tuples) into a pandas DataFrame (like a table)
# The DataFrame will have three columns: placename, month, and count
df = pd.DataFrame(rows_to_write, columns=["placename", "month", "count"])

# Create a DataFrame and save it to a TSV file for later mapping
df = pd.DataFrame(rows_to_write, columns=["placename", "month", "count"])
df.to_csv("../scripts/data/regex_counts.tsv", sep="\t", index=False)
