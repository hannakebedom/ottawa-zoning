# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

import folium
from folium.plugins import Geocoder, TimestampedGeoJson
from arcgis.features import FeatureLayer
from pyproj import Transformer
from shapely.geometry import Polygon
import datetime

OTTAWA = [45.4215, -75.6972]
RIVERSIDE = [45.2815, 75.6832]

# City of Ottawa Zoning: https://ottawa.ca/en/living-ottawa/laws-licences-and-permits/laws/laws-z/zoning-law-no-2008-250/zoning-law-2008-250-consolidation#
RESIDENTIAL_ZONES = {"R1", "R2", "R3", "R4", "R5", "RM"}
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
    '''get map color associated with a particular type of zone'''
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

def create_timeline_map(features):
    '''creates a folium map that divides zones into layers based on consolidation year'''

    # create basemap
    m = folium.Map(location=RIVERSIDE, zoom_start=10)

    # initialize layers for each year
    features_2008 = []
    features_2008_2009 = [[]]
    features_2009 = []
    features_2009_2010 = [[]] 
    features_2010 = []
    features_2010_2011 = [[]] 
    features_2011 = []
    features_2011_2012 = [[]]
    features_2012 = []
    features_2012_2013 = [[]]
    features_2013 = []
    features_2013_2014 = [[]]
    features_2014 = []
    features_2014_2015 = [[]]
    features_2015 = []
    features_2015_2016 = [[]]
    features_2016 = []
    features_2016_2017 = [[]]
    features_2017 = []
    features_2017_2018 = [[]]
    features_2018 = []
    features_2018_2019 = [[]]
    features_2019 = []
    features_2019_2020 = [[]]
    features_2020 = []
    features_2020_2021 = [[]]
    features_2021 = []

    yearly_layers = [features_2008, features_2008_2009, features_2009, features_2009_2010, features_2010, features_2010_2011, features_2011, features_2011_2012, features_2012, features_2012_2013, features_2013, features_2013_2014, features_2014, features_2014_2015, features_2015, features_2015_2016, features_2016, features_2016_2017, features_2017, features_2017_2018, features_2018, features_2018_2019, features_2019, features_2019_2020, features_2020, features_2020_2021, features_2021]

    # organize features into layers based on consolidation date
    for feature in features:
        coordinates = convert_crs(feature.geometry['rings'][0])
        date = feature.attributes["CONS_DATE"]
        for i in range(len(coordinates)):
            coordinates[i][0], coordinates[i][1] = coordinates[i][1], coordinates[i][0]
        if date.endswith("2008"):
            features_2008.append([coordinates])
        elif date.endswith("2009"):
            features_2009.append([coordinates])
        elif date.endswith("2010"):
            features_2010.append([coordinates])
        elif date.endswith("2011"):
            features_2011.append([coordinates])
        elif date.endswith("2012"):
            features_2012.append([coordinates])
        elif date.endswith("2013"):
            features_2013.append([coordinates])
        elif date.endswith("2014"):
            features_2014.append([coordinates])
        elif date.endswith("2015"):
            features_2015.append([coordinates])
        elif date.endswith("2016"):
            features_2016.append([coordinates])
        elif date.endswith("2017"):
            features_2017.append([coordinates])
        elif date.endswith("2018"):
            features_2018.append([coordinates])
        elif date.endswith("2019"):
            features_2019.append([coordinates])
        elif date.endswith("2020"):
            features_2020.append([coordinates])
        elif date.endswith("2021"):
            features_2021.append([coordinates])

    # compute intersection of layers from year-to-year (to visalize differences)
    for i in range(len(yearly_layers)-2):
        layer_a = yearly_layers[i]
        layer_b = yearly_layers[i + 2]
        for f1 in layer_a:
            for f2 in layer_b:
                intersection = None
                try:
                    p1, p2 = Polygon(f1[0]), Polygon(f2[0])
                    if p1.touches(p2) or p2.touches(p1): continue
                    if p1.intersects(p2):
                        if p1.within(p2):
                            intersection = p1
                        elif p2.within(p1):
                            intersection = p2
                        else:
                            print("applying sutherland hodgman . . .")
                            area = p1.intersection(p2).area
                            if area > 0.0000001:
                                intersection = sutherland_hodgman(p1.exterior.coords, p2.exterior.coords)
                except Exception as e:
                    print("an error occurred:", e)
                if intersection:
                    print("drawing intersection . . .")              
                    intersection_polygon = Polygon(intersection)
                    yearly_layers[i + 1].append(list(intersection_polygon.exterior.coords))
                    # folium.Polygon(locations=intersection_polygon.exterior.coords, color="#faff00", fill=True, fill_color="#faff00", fill_opacity=0.7).add_to(yearly_layers[i + 1])

    features = []
    curr_year = 2008
    colors = { 2008: "#f94144", 2009: "#f3722c", 2010: "#f8961e", 2011: "#f9844a", 2012: "#f9c74f", 2013: "#90be6d", 2014: "#90be6d", 2015: "#43aa8b", 2016: "#4d908e", 2017: "#577590", 2018: "#277da1", 2019: "#54478c", 2020: "#bd4f6c", 2021: "#905a51"}
    overlap_color = "#ffff24"

    for i in range(len(yearly_layers)):

        if i % 2 != 0:
            print("overlap length: ", len(yearly_layers[i][0]))
            color = overlap_color
        else:
            color = colors[curr_year]

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": yearly_layers[i]
                },
                "properties": {
                    "times": [datetime.datetime(curr_year, 1, 1).isoformat()] * len(yearly_layers[i]),
                    "style": {
                        "color": color,
                        "fillColor": color,
                        "fillOpacity": 0.5
                    }
                },
            }
        )

        if i % 2 == 0:
            curr_year += 1

    TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        period="P1Y",
        transition_time=1000
    ).add_to(m)

    # add search to map
    Geocoder().add_to(m)

    # add legend
    folium.LayerControl().add_to(m)

    # save map to data folder
    m.save("maps/map-timeTEST.html")

def create_zone_map(features):
    '''creates a folium map that splits features into layers based on types of zones'''

    # create basemap
    m = folium.Map(location=OTTAWA, zoom_start=13)

    # create map title
    title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format("City of Ottawa Zones by Type")

    # initialize layers for each type of zone
    fg_residential = folium.FeatureGroup(name="Residential Zones")
    fg_institutional = folium.FeatureGroup(name="Institutional Zones")
    fg_open_space = folium.FeatureGroup(name="Open Space Leisure Zones")
    fg_environmental = folium.FeatureGroup(name="Environmental Zones")
    fg_commercial = folium.FeatureGroup(name="Commercial Zones")
    fg_industrial = folium.FeatureGroup(name="Industrial Zones")
    fg_transportation = folium.FeatureGroup(name="Transportation Zones")
    fg_rural = folium.FeatureGroup(name="Rural Zones")
    fg_other = folium.FeatureGroup(name="Other Zones")

    for feature in features:
        coordinates = convert_crs(feature.geometry['rings'][0])
        zone = feature.attributes["PARENTZONE"]
        color = get_color(zone)

        polygon = folium.Polygon(locations=coordinates, color=color, fill=True, fill_color=color, fill_opacity=0.5)

        if zone in RESIDENTIAL_ZONES:
            polygon.add_to(fg_residential)
        elif zone in INSTITUTIONAL_ZONES:
            polygon.add_to(fg_institutional)
        elif zone in OPEN_SPACE_LEISURE_ZONES:
            polygon.add_to(fg_open_space)
        elif zone in ENVIRONMENTAL_ZONES:
            polygon.add_to(fg_environmental)
        elif zone in COMMERICAL_ZONES:
            polygon.add_to(fg_commercial)
        elif zone in INDUSTRIAL_ZONES:
            polygon.add_to(fg_industrial)
        elif zone in TRANSPORTATION_ZONES:
            polygon.add_to(fg_transportation)
        elif zone in RURAL_ZONES:
            polygon.add_to(fg_rural)
        elif zone in OTHER_ZONES:
            polygon.add_to(fg_other)

    # add layers to map    
    fg_residential.add_to(m)
    fg_institutional.add_to(m)
    fg_open_space.add_to(m)
    fg_environmental.add_to(m)
    fg_commercial.add_to(m)
    fg_industrial.add_to(m)
    fg_transportation.add_to(m)
    fg_rural.add_to(m)
    fg_other.add_to(m)

    # add search bar to map
    Geocoder().add_to(m)

    # add legend to map 
    folium.LayerControl().add_to(m)

    # add title to map
    m.get_root().html.add_child(folium.Element(title_html))

    # save map to data folder
    m.save("maps/map-zone.html")

def same_side(edge_start, edge_end, p):
    '''given an edge and a point determine if the point lies on the same side as the rest of the polygon'''
    return (edge_end[0] - edge_start[0]) * (p[1] - edge_start[1]) <= (edge_end[1] - edge_end[1]) * (p[0] - edge_start[0])

def intersection(p1, p2, p3, p4):
    '''find the intersection point between two lines that intersect'''
    x = ( (p1[0]*p2[1]-p1[1]*p2[0])*(p3[0]-p4[0])-(p1[0]-p2[0])*(p3[0]*p4[1]-p3[1]*p4[0]) ) / ( (p1[0]-p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]-p4[0]) )
    y = ( (p1[0]*p2[1]-p1[1]*p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]*p4[1]-p3[1]*p4[0]) ) / ( (p1[0]-p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]-p4[0]) )
    return (x, y)

def sutherland_hodgman(subject_polygon,clipping_polygon):
    '''implementation of the sutherland hodgman clipping algorithm'''
    output_polygon = subject_polygon[:]
    clip_edges = [tuple(clipping_polygon[i:i+2]) for i in range(len(clipping_polygon)-1)]
    
    for clip_edge in clip_edges:
        subject_polygon = Polygon(output_polygon[:]).exterior.coords # cast as shapely polygon to ensure that vertices are listed in clockwise order
        subject_edges = [tuple(subject_polygon[i:i+2]) for i in range(len(subject_polygon)-1)]
        output_polygon = []
        clip_start, clip_end  = clip_edge[0], clip_edge[1]
        
        for subject_edge in subject_edges:
            subject_start, subject_end = subject_edge[0], subject_edge[1]
            if same_side(clip_start, clip_end, subject_end):
                if not same_side(clip_start, clip_end, subject_start):
                    intersection_point = intersection(clip_start, clip_end, subject_start, subject_end)
                    output_polygon.append(intersection_point)
                output_polygon.append(tuple(subject_end))
            elif same_side(clip_start, clip_end,subject_start):
                intersection_point = intersection(clip_start, clip_end, subject_start, subject_end)
                output_polygon.append(intersection_point)
    
    return output_polygon

def main():
    print("starting .. ")
    features = get_features()
    print("retrieved " + str(len(features)) + " features")
    create_zone_map(features)
    create_timeline_map(features)

if __name__ == "__main__":
    main()
