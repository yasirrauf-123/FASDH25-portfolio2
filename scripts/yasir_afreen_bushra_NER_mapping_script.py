"""
This script is part of our Digital Humanities course Mini Project No. 2, where we explore how to visualize
the places mentioned in news articles over time. Using computational tools, we extract toponyms (place names)
from each article, map them, and observe how the geographic focus of the news shifts over time.

In this script, we use the output generated from the Gaza_NER2_yasir_afreen_bushra collab notebook (a .tsv file containing the monthly count of places)
and the NER_gazetteer from the build_gazetteer collab notebook of our mini project No. 2. We merge these files because the NER_counts
file does not contain coordinates, which are essential for mapping, while the NER_gazetteer file provides the geographic
coordinates for these places. By merging the datasets, we combine the place counts with their respective geographic coordinates, enabling us to map the locations.
"""

# Help was taken from ChatGPT and mapping presentation slides to come up with this code (see ChatGPT Solution No.13 in AI Documentation)
# Importing necessary libraries for data manipulation and plotting
import os
import pandas as pd
import plotly.express as px

# Ensure the output directory exists
os.makedirs("../scripts/output", exist_ok=True)

# Loading the NER counts and geographic data from TSV files
counts = pd.read_csv("../scripts/data/ner_counts.tsv", sep="\t")
coords = pd.read_csv("../scripts/data/NER_gazetteer.tsv", sep="\t")

# Renaming columns in coords to match the ones in counts for easier merging
coords = coords.rename(columns={
    "Name": "placename",
    "Latitude": "latitude",
    "Longitude": "longitude"
})

# Merging the two dataframes on the common 'placename' column
data = pd.merge(counts, coords, on="placename")

# Converting 'count' to numeric and removing rows with missing data
data["count"] = pd.to_numeric(data["count"], errors="coerce")
data = data.dropna(subset=["count", "latitude", "longitude"])

# Creating an interactive map using plotly, with place names, counts, and geographic coordinates
fig = px.scatter_map(
    data,
    lat="latitude",  # Latitude column
    lon="longitude",  # Longitude column
    hover_name="placename",  # Display the place name on hover
    size="count",  # Size of points based on the count
    color="count",  # Color of points based on the count
    title="NER-extracted Place Names (Jan 2024)"  # Title of the map
)

# Saving the map as an interactive HTML file and static PNG image
fig.write_html("NER_map.html")
fig.write_image("NER_map.png")

# Saving the map in the output folder
fig.write_html("../scripts/output/NER_map.html")  # Save HTML
fig.write_image("../scripts/output/NER_map.png")  # Save PNG

# Displaying the map
fig.show()
