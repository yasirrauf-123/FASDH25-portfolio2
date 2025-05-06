"""
This script is part of our Digital Humanities course Mini Project No. 2, where we explore how to visualize
the places mentioned in news articles over time. Using computational tools, we extract toponyms (place names)
from each article, map them, and observe how the geographic focus of the news shifts over time.

In this script, we use the output generated from the regex_script_final file (a .tsv file containing the monthly count of places)
and the geoname_gaza_selections file from the gazetteer folder of our mini project No. 2. We merge these files because the regex_counts
file does not contain coordinates, which are essential for mapping, while the geoname_gaza_selections file provides the geographic
coordinates for these places. By merging the datasets, we combine the place counts with their respective geographic coordinates, enabling us to map the locations.
"""

# Help was taken from ChatGPT and mapping slides presentation to draft the comments and code (See ChatGPT Solution No. 12 in AI Documentation)
# Import required libraries
import pandas as pd  # Import pandas for data manipulation and analysis
import plotly.express as px  # Import plotly.express for creating interactive plots

# Load data from CSV files
counts = pd.read_csv("../scripts/regex_counts.tsv", sep="\t")  # Load the regex counts data
coords = pd.read_csv("../gazetteers/geonames_gaza_selection.tsv", sep="\t")  # Load the geographical coordinates data

# Rename columns for consistency to match the columns in the counts dataset
coords = coords.rename(columns={  # Rename columns for better readability
    "asciiname": "placename",  # Rename 'asciiname' to 'placename' to match the 'counts' dataset
    "latitude": "latitude",  # Keep 'latitude' as is
    "longitude": "longitude"  # Keep 'longitude' as is
})

# Merge the counts data with the geographical coordinates data based on the 'placename' column
data = pd.merge(counts, coords, on="placename")  # Merge the two datasets based on the 'placename' column

# Convert the 'count' column to numeric values, coercing errors to NaN (if any non-numeric values are present)
data["count"] = pd.to_numeric(data["count"], errors="coerce")  # Convert the 'count' column to numeric format
data = data.dropna(subset=["count", "latitude", "longitude"])  # Drop rows with missing 'count', 'latitude', or 'longitude' values

# Create an animated map using Plotly Express
fig = px.scatter_map(  # Create a scatter map with Plotly Express
    data,  # The data to plot
    lat="latitude",  # Use 'latitude' for the y-axis (latitude)
    lon="longitude",  # Use 'longitude' for the x-axis (longitude)
    hover_name="placename",  # Display the 'placename' when hovering over a point
    size="count",  # Use the 'count' column to determine the size of the points on the map
    animation_frame="month",  # Create an animation based on the 'month' column
    color="count",  # Color the points based on the 'count' value
    color_continuous_scale=px.colors.sequential.YlOrRd,  # Set the color scale to 'YlOrRd' (yellow-orange-red)
    title="Regex-Extracted Place Names by Month"  # Set the title of the map
)

# Save the animated map as HTML and PNG files
fig.write_html("regex_map.html")  # Save the interactive map as an HTML file
fig.write_image("regex_map.png")  # Save the map as a PNG image

# Display the map
fig.show()  # Show the interactive map in the notebook

