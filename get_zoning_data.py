from arcgis.features import FeatureLayer
from IPython.display import display

layer_url = "https://services8.arcgis.com/j9ezxktwsGMiHmNz/ArcGIS/rest/services/City_of_Ottawa_Zoning/FeatureServer/0"
layer = FeatureLayer(layer_url)
print(layer)
