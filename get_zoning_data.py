# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

from arcgis.features import FeatureLayer
from IPython.display import display

feature_layer_url = "https://services8.arcgis.com/j9ezxktwsGMiHmNz/ArcGIS/rest/services/City_of_Ottawa_Zoning/FeatureServer/0"
feature_layer = FeatureLayer(feature_layer_url)

# list properties of the layer
for f in feature_layer.properties.fields:
    print(f['name'])

# list the attributes of the first feature
feature_set = feature_layer.query()
features = feature_set.features

# each feature consists of a set of rings (points) that define the polygon
print(features[0].attributes)
print(features[0].geometry)

# NEXT: https://gis.stackexchange.com/questions/294206/how-to-create-a-simple-polygon-from-coordinates-in-geopandas-with-python

