# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

import folium
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.geometry import Polygon
import geopandas as gpd
# from shapely.geometry import Polygon
from IPython.display import display
import numpy as np
import webbrowser

feature_layer_url = "https://services8.arcgis.com/j9ezxktwsGMiHmNz/ArcGIS/rest/services/City_of_Ottawa_Zoning/FeatureServer/0"
feature_layer = FeatureLayer(feature_layer_url)
feature_set = feature_layer.query()
features = feature_set.features

geometry = features[0].geometry
polygon = Polygon(geometry)


# TODO: Try using the ArcGIS map widget instead of Folium: 
#   https://developers.arcgis.com/python/guide/part1-introduction-to-using-the-map-widget/
#   https://developers.arcgis.com/python/guide/part2-working-with-geometries/
# FOLIUM: https://gis.stackexchange.com/questions/294206/how-to-create-a-simple-polygon-from-coordinates-in-geopandas-with-python

