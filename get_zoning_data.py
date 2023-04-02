# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

import folium
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.geometry import Polygon
import pyproj

def get_features(feature_layer_url = "https://services8.arcgis.com/j9ezxktwsGMiHmNz/ArcGIS/rest/services/City_of_Ottawa_Zoning/FeatureServer/0"):
    '''retrieve features from the specified url'''
    feature_layer = FeatureLayer(feature_layer_url)
    feature_set = feature_layer.query()
    features = feature_set.features
    return features

# convert the coordinates to latitude and longitude
lon_lat = []
for ring in geometry['rings']:
    lon_lat.append([pyproj.transform(in_proj, out_proj, x, y) for x, y in ring])



# main 
print(geometry)
polygon = Polygon(geometry)



