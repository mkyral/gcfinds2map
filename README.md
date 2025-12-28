# gcfinds2map

Create a map image showing yours geocache finds.
A replacement for no more working "mapicky" from geocaching.cz

![An example map](doc/example_map.png)

You will need your Geocache finds from pocket query.

Usage:
```shell
python gcfinds2map.py pocket_query_gpx_file
```

This is implemented with geopandas library: https://geopandas.org

The geojson files were generated from OpenStreetMap via overpass-turbo.
