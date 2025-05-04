"""
This is the starting script for today's class,
in which we'll build our first maps in Python.
"""
import pandas as pd
import plotly.express as px

# Load data
counts = pd.read_csv("../scripts/ner_counts.tsv", sep="\t")
coords = pd.read_csv("../scripts/NER_gazetteer.tsv", sep="\t")

# Merge data on 'placename'
data = pd.merge(counts, coords, on="placename")

# Plot map
fig = px.scatter_geo(
    data,
    lat="latitude",
    lon="longitude",
    hover_name="placename",
    size="count",
    projection="natural earth",
    title="NER-extracted Place Names (Jan 2024)",
)

fig.show()

