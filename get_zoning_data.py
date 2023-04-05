# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

import folium
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.geometry import Polygon
from pyproj import Transformer
from folium.plugins import MarkerCluster, FeatureGroupSubGroup
from collections import defaultdict
from datetime import datetime

OTTAWA = [45.4215, -75.6972]

# City of Ottawa Zoning: https://ottawa.ca/en/living-ottawa/laws-licences-and-permits/laws/laws-z/zoning-law-no-2008-250/zoning-law-2008-250-consolidation#
RESIDENTIAL_ZONES = {"R1", "R2", "R3", "R4", "R5", "RM"} # brown
INSTITUTIONAL_ZONES = {"I1", "I2"}
OPEN_SPACE_LEISURE_ZONES = {"L1", "L2", "L3", "O1"}
ENVIRONMENTAL_ZONES = {"EP"}
COMMERICAL_ZONES = {"AM", "GM", "LC", "MC", "MD", "TD", "TM"}
INDUSTRIAL_ZONES = {"IG", "IH", "IL", "IP"}
TRANSPORTATION_ZONES = {"T1", "T2"}
RURAL_ZONES = {"AG", "ME", "MR", "RC", "RG", "RH", "RI", "RR", "RU", "VM", "V1", "V2", "V3"}
OTHER_ZONES = {"DR"}

def get_features(feature_layer_url = "https://services8.arcgis.com/j9ezxktwsGMiHmNz/ArcGIS/rest/services/City_of_Ottawa_Zoning/FeatureServer/0"):
    '''retrieve features from the specified url'''
    feature_layer = FeatureLayer(feature_layer_url)
    feature_set = feature_layer.query()
    features = feature_set.features
    return features

def convert_crs(coordinates, fro="EPSG:3857", to="EPSG:4326"):
    '''convert coordinates from one reference system to another'''
    transformer = Transformer.from_crs(fro, to)
    result = []
    for x, y in coordinates:
        result.append(list(transformer.transform(x, y)))
    return result

def get_color(zone):
    color = "#e5e5e5"
    if zone in RESIDENTIAL_ZONES:
        color = "#00bbf9" # blue
    elif zone in INSTITUTIONAL_ZONES:
        color = "#7209b7" # violet
    elif zone in OPEN_SPACE_LEISURE_ZONES:
        color = "#ff0054" # pink
    elif zone in ENVIRONMENTAL_ZONES:
        color = "#59e800" # green
    elif zone in COMMERICAL_ZONES:
        color = "#ffbd00" # yellow
    elif zone in INDUSTRIAL_ZONES:
        color = "#80ffdb" # turquoise
    elif zone in TRANSPORTATION_ZONES:
        color = "#d00000" # red
    elif zone in RURAL_ZONES:
        color = "#fb5607" # orange
    elif zone in OTHER_ZONES:
        color = "#274c77" # navy
    return color

def add_to_layers(zone, polygon, residential):
    if zone in RESIDENTIAL_ZONES:
        polygon.add_to(residential)

def create_timeline_map(features):
    m = folium.Map(location=OTTAWA, zoom_start=13)
    fg_2008 = folium.FeatureGroup(name="2008")
    fg_2009 = folium.FeatureGroup(name="2009")
    fg_2010 = folium.FeatureGroup(name="2010")
    fg_2011 = folium.FeatureGroup(name="2011")
    fg_2012 = folium.FeatureGroup(name="2012")
    fg_2013 = folium.FeatureGroup(name="2013")
    fg_2014 = folium.FeatureGroup(name="2014")
    fg_2015 = folium.FeatureGroup(name="2015")
    fg_2016 = folium.FeatureGroup(name="2016")
    fg_2017 = folium.FeatureGroup(name="2017")
    fg_2018 = folium.FeatureGroup(name="2018")
    fg_2019 = folium.FeatureGroup(name="2019")
    fg_2020 = folium.FeatureGroup(name="2020")
    fg_2021 = folium.FeatureGroup(name="2021")

    for feature in features:
        coordinates = convert_crs(feature.geometry['rings'][0])
        date = feature.attributes["CONS_DATE"]
        if date.endswith("2008"):
            folium.Polygon(locations=coordinates, color="#ff0000", fill=True, fill_color="#ff0000", fill_opacity=0.5).add_to(fg_2008)
        elif date.endswith("2009"):
            folium.Polygon(locations=coordinates, color="#ff8700", fill=True, fill_color="#ff8700", fill_opacity=0.5).add_to(fg_2009)
        elif date.endswith("2010"):
            folium.Polygon(locations=coordinates, color="#ffd300", fill=True, fill_color="#ffd300", fill_opacity=0.5).add_to(fg_2010)
        elif date.endswith("2011"):
            folium.Polygon(locations=coordinates, color="#deff0a", fill=True, fill_color="#deff0a", fill_opacity=0.5).add_to(fg_2011)
        elif date.endswith("2012"):
            folium.Polygon(locations=coordinates, color="#a1ff0a", fill=True, fill_color="#a1ff0a", fill_opacity=0.5).add_to(fg_2012)
        elif date.endswith("2013"):
            folium.Polygon(locations=coordinates, color="#0aff99", fill=True, fill_color="#0aff99", fill_opacity=0.5).add_to(fg_2013)
        elif date.endswith("2014"):
            folium.Polygon(locations=coordinates, color="#0aefff", fill=True, fill_color="#0aefff", fill_opacity=0.5).add_to(fg_2014)
        elif date.endswith("2015"):
            folium.Polygon(locations=coordinates, color="#147df5", fill=True, fill_color="#147df5", fill_opacity=0.5).add_to(fg_2015)
        elif date.endswith("2016"):
            folium.Polygon(locations=coordinates, color="#580aff", fill=True, fill_color="#580aff", fill_opacity=0.5).add_to(fg_2016)
        elif date.endswith("2017"):
            folium.Polygon(locations=coordinates, color="#be0aff", fill=True, fill_color="#be0aff", fill_opacity=0.5).add_to(fg_2017)
        elif date.endswith("2018"):
            folium.Polygon(locations=coordinates, color="#7b4618", fill=True, fill_color="#7b4618", fill_opacity=0.5).add_to(fg_2018)
        elif date.endswith("2019"):
            folium.Polygon(locations=coordinates, color="#606f49", fill=True, fill_color="#606f49", fill_opacity=0.5).add_to(fg_2019)
        elif date.endswith("2020"):
            folium.Polygon(locations=coordinates, color="#b4418e", fill=True, fill_color="#b4418e", fill_opacity=0.5).add_to(fg_2020)
        elif date.endswith("2021"):
            folium.Polygon(locations=coordinates, color="#ea515f", fill=True, fill_color="#ea515f", fill_opacity=0.5).add_to(fg_2021)
    
    fg_2008.add_to(m)
    fg_2009.add_to(m)
    fg_2010.add_to(m)
    fg_2011.add_to(m)
    fg_2012.add_to(m)
    fg_2013.add_to(m)
    fg_2014.add_to(m)
    fg_2015.add_to(m)
    fg_2016.add_to(m)
    fg_2017.add_to(m)
    fg_2018.add_to(m)
    fg_2019.add_to(m)
    fg_2020.add_to(m)
    fg_2021.add_to(m)

    folium.LayerControl().add_to(m)
    m.save("data/map-time.html")










def create_zone_map(features):
    '''creates a folium map'''
    m = folium.Map(location=OTTAWA, zoom_start=13)
    fg_all_zones = folium.FeatureGroup(name="All Zones")

    dates = defaultdict(int)
    bylaw_nums = defaultdict(int)


    for feature in features:
        coordinates = convert_crs(feature.geometry['rings'][0])
        id = feature.attributes["FID"]
        date = feature.attributes["CONS_DATE"]
        bylaw_num = feature.attributes["BYLAW_NUM"]
        zone = feature.attributes["PARENTZONE"]
        history = feature.attributes["HISTORY"]

        dates[date] += 1
        bylaw_nums[bylaw_num] += 1
        date_obj = date

        # color = get_color(zone)
        # polygon = folium.Polygon(locations=coordinates, color=color, fill=True, fill_color=color, fill_opacity=0.5)
        # polygon.add_to(fg_all_zones)
        
        # Intersection of Carp Rd. and Donald B. Munro Dr.
        # id: 2018-171
        # history: 2012-033, 2013-058
    print("dates", dates)
    print("bylaw nums", bylaw_num)

    fg_all_zones.add_to(m)
    folium.LayerControl().add_to(m)
    m.save("data/map.html")

def main():
    # get features from City of Ottawa resource
    print("starting .. ")
    features = get_features()
    print("retrieved " + str(len(features)) + " features")
    # create a map from given features
    # create_zone_map(features)
    create_timeline_map(features)

if __name__ == "__main__":
    main()
