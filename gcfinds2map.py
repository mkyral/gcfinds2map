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
import os.path
import zipfile
import geopandas as gpd
#import geodatasets
import folium
import matplotlib.pyplot as plt

# Read input parameters
program_name = sys.argv[0]
arguments = sys.argv[1:]

# Check number of arguments
if (len(arguments) < 1):
    print("Usage: %s <my_finds_file>" % (program_name))
    exit(1)


# Verify that file exists
if (not os.path.isfile(arguments[0])):
    print("Error: %s is not a file" % arguments[0])
    exit(1)

#
# Load data files
#

# Geocache finds (pocket query)
my_finds_gpx = arguments[0]

if (len(arguments) > 1):
    out_file = arguments[1]
else:
    out_file = "my_finds.png"

# Load from zip archive
if (zipfile.is_zipfile(my_finds_gpx)):
    try:
        archive = zipfile.ZipFile(my_finds_gpx, 'r')
        gpx = gpd.read_file(archive.open(archive.namelist()[0]))
    except:
        print("Error: Can't open zip file!")
        exit(1)
else: # Load as gpx file
    gpx = gpd.read_file(my_finds_gpx)

# Czech Republic contour (admin_level=2)
contour = gpd.read_file("data/cr.geojson")

# Czech Republic division (admin_level=4)
division = gpd.read_file("data/cr_kraje.geojson")


# Ensure coordinates system is the same
gpx = gpx.to_crs(contour.crs)

# Limit finds to Czech Republic border box
xmin, ymin, xmax, ymax = contour.total_bounds
filtered_gpx = gpx.cx[xmin:xmax, ymin:ymax]

# Plot grey divisions
base = division.plot(figsize=(10, 7), color="none", edgecolor="darkgrey", markersize=0)

# Plot contour
base = contour.plot(ax=base, figsize=(10, 7), color="none", edgecolor="black")

# Plot finds
filtered_gpx.plot(ax=base, marker="*", color='red', markersize=1);

# Hide axis
plt.axis('off')

# Save image, remove axis padding
plt.savefig(out_file, bbox_inches='tight', pad_inches=0)

print("File %s generated" % out_file)

# Show generated plot
#plt.show()


