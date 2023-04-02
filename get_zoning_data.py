# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

import folium
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.geometry import Polygon
import pyproj

feature_layer_url = "https://services8.arcgis.com/j9ezxktwsGMiHmNz/ArcGIS/rest/services/City_of_Ottawa_Zoning/FeatureServer/0"
feature_layer = FeatureLayer(feature_layer_url)
feature_set = feature_layer.query()
features = feature_set.features
geometry = features[0].geometry

# define the projection systems
in_proj = pyproj.Proj(init='epsg:3857')
out_proj = pyproj.Proj(init='epsg:4326')

# convert the coordinates to latitude and longitude
lon_lat = []
for ring in geometry['rings']:
    lon_lat.append([pyproj.transform(in_proj, out_proj, x, y) for x, y in ring])




print(geometry)
polygon = Polygon(geometry)


# TODO: Try using the ArcGIS map widget instead of Folium: 
#   https://developers.arcgis.com/python/guide/part1-introduction-to-using-the-map-widget/
#   https://developers.arcgis.com/python/guide/part2-working-with-geometries/
# FOLIUM: https://gis.stackexchange.com/questions/294206/how-to-create-a-simple-polygon-from-coordinates-in-geopandas-with-python

