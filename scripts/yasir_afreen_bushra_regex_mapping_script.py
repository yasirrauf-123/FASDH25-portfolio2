import pandas as pd
import plotly.express as px

# Load data
counts = pd.read_csv("../scripts/regex_counts.tsv", sep="\t")
coords = pd.read_csv("../gazetteers/geonames_gaza_selection.tsv", sep="\t")

# Clean column names
counts.columns = counts.columns.str.strip()
coords.columns = coords.columns.str.strip()

# Rename for consistency
coords = coords.rename(columns={
    "asciiname": "placename",
    "latitude": "latitude",
    "longitude": "longitude"
})

# Merge
data = pd.merge(counts, coords, on="placename")

# Clean numeric values
data["count"] = pd.to_numeric(data["count"], errors="coerce")
data = data.dropna(subset=["count", "latitude", "longitude"])

# Create animated map
fig = px.scatter_geo(
    data,
    lat="latitude",
    lon="longitude",
    hover_name="placename",
    size="count",
    animation_frame="month",
    projection="natural earth",
    title="Regex-Extracted Place Names by Month"
)

# Save outputs
fig.write_html("regex_map.html")
fig.write_image("regex_map.png")

# Show the map
fig.show()
