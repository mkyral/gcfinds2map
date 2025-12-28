#!/usr/bin/python
"""Generate map with geocache finds.

Create a map image showing yours geocache finds.
A replacement for no more working "mapicky" from geocaching.cz

This is implemented with geopandas library: https://geopandas.org

The geojson files were generated from OpenStreetMap via overpass-turbo.

More info on
 Github: https://github.com/mkyral/gcfinds2map
"""

import sys
import geopandas as gpd
#import geodatasets
import folium
import matplotlib.pyplot as plt

# Read input parameters
program_name = sys.argv[0]
arguments = sys.argv[1:]

if (len(arguments) < 1):
    print("Usage: %s my_finds_pocket_query_gpx_file" % (program_name))
    exit(1)

my_finds_gpx = arguments[0]

# Load data
# Czech Republic contour (admin_level=2)
cr_map = gpd.read_file("data/cr.geojson")

# Czech Republic division (admin_level=4)
kraje = gpd.read_file("data/cr_kraje.geojson")

# Geocache finds (pocket query)
gpx = gpd.read_file(my_finds_gpx)

# Ensure coordinates system is the same
gpx = gpx.to_crs(cr_map.crs)

# Limit finds to Czech Republic border box
xmin, ymin, xmax, ymax = cr_map.total_bounds
filtered_gpx = gpx.cx[xmin:xmax, ymin:ymax]

# Plot grey divisions
base = kraje.plot(figsize=(10, 7), color="none", edgecolor="darkgrey", markersize=0)

# Plot contour
base = cr_map.plot(ax=base, figsize=(10, 7), color="none", edgecolor="black")

# Plot finds
filtered_gpx.plot(ax=base, marker="*", color='red', markersize=1);

# Hide axis
plt.axis('off')

# Save image, remove axis padding
plt.savefig("nalezy.png", bbox_inches='tight', pad_inches=0)

# Show generated plot
#plt.show()


