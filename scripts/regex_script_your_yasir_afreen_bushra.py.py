'''This is your starting script for today's Python class.

This script contains the code we wrote last week
to count the number of times each place in Gaza
is mentioned in our corpus.

Now, we want to store this count into a tsv file.

I have written a function (write csv) to do this -
but it has some mistakes in it.

Please fix the mistakes and call the function
to write the 

'''
import re
import os
import pandas as pd


war_start_date = "2023-10-07"
def write_tsv(data, column_list, path):
    """This function converts a dictionary to a tsv file.

    It takes three arguments:
        data (dict): the dictionary
        column_list (list): a list of column names
        path (str): the path to which the tsv file will be written
    """
   
    # turn the dictionary into a list of (key, value) tuples (this is correct):
    
    # create a dataframe from the items list (this is correct):
    df = pd.DataFrame(data, columns=column_list)
    # write the dataframe to tsv:
    df.to_csv(path, sep="\t", index=False)


# define which folder to use:
folder = "../articles"  

# define the patterns we want to search:

# load the gazetteer from the tsv file:
path = "../gazetteers/geonames_gaza_selection.tsv"
with open(path, encoding="utf-8") as file:
    data = file.read()

rows = data.strip().split("\n")

# build a dictionary of patterns from the place names in the first column:
patterns = {}
mentions_per_month = {}
for row in rows[1:]:
    if not row.strip():
        continue  
    columns = row.split("\t")
    asciiname = columns[0].strip()

    alt_names = []
    for col in columns:
        alt_names.extend(col.strip().split(","))

    alt_names = list(set(name.strip() for name in alt_names if name.strip()))
    if not alt_names:
        continue

    regex_pattern = "|".join(re.escape(name) for name in alt_names)
    patterns[asciiname] = regex_pattern


# count the number of times each pattern is found in the entire folder:
for filename in os.listdir(folder):
     article_date = filename.split("_")[0]
     if article_date < war_start_date:
        continue
     file_path = os.path.join(folder, filename)
     with open(file_path, encoding="utf-8") as file:
        text = file.read()
     for name, regex_pattern in patterns.items():
        matches = re.findall(regex_pattern, text, flags=re.IGNORECASE)
        n_matches = len(matches)
        if n_matches == 0:
            continue
        month = article_date[:7]  
        if name not in mentions_per_month:
            mentions_per_month[name] = {}
        if month not in mentions_per_month[name]:
            mentions_per_month[name][month] = 0
        mentions_per_month[name][month] += n_matches

# print the frequency of each pattern:
for place, months in mentions_per_month.items():
    for month, count in months.items():
        if count >= 1:
            print(f"Found {place} {count} times in {month}")

# call the function to write your tsv file:
tsv_data = []
for place, months in mentions_per_month.items():
    for month, count in months.items():
        tsv_data.append([place, month, count])
write_tsv(tsv_data, ["placename", "month", "count"], "regex_counts.tsv")

        
