# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

import folium
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.geometry import Polygon
from pyproj import Transformer

OTTAWA = [45.4215, -75.6972]

def get_features(feature_layer_url = "https://services8.arcgis.com/j9ezxktwsGMiHmNz/ArcGIS/rest/services/City_of_Ottawa_Zoning/FeatureServer/0"):
    '''retrieve features from the specified url'''
    feature_layer = FeatureLayer(feature_layer_url)
    feature_set = feature_layer.query()
    features = feature_set.features
    return features

def convert_crs(coordinates, fro="EPSG:3857", to="EPSG:4326"):
    '''convert coordinates from one reference system to another'''
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")
    result = []
    for x, y in coordinates:
        result.append(list(transformer.transform(x, y)))
    return result

def create_map(features):
    '''creates a folium map'''
    m = folium.Map(location=OTTAWA, zoom_start=13)
    for feature in features:
        coordinates = convert_crs(feature.geometry['rings'][0])
        folium.Polygon(locations=coordinates, color='blue', fill=True, fill_color='blue').add_to(m)
    m.save("data/map.html")

def main():
    # get features from City of Ottawa resource
    features = get_features()
    # create a map from given features
    create_map(features)

if __name__ == "__main__":
    main()
