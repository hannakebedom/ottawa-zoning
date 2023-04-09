# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

import folium
from arcgis.features import FeatureLayer
from pyproj import Transformer
from folium.plugins import Geocoder
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection

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

def area(polygon1, polygon2):
    '''returns the area of the intersection of two polygons'''

def create_timeline_map(features):
    m = folium.Map(location=OTTAWA, zoom_start=13)
    fg_2008, features_2008 = folium.FeatureGroup(name="2008"), []
    fg_2008_2009 = folium.FeatureGroup(name="2008/2009", show=False)
    fg_2009, features_2009 = folium.FeatureGroup(name="2009"), []
    fg_2009_2010 = folium.FeatureGroup(name="2009/2010", show=False)
    fg_2010, features_2010 = folium.FeatureGroup(name="2010"), []
    fg_2010_2011 = folium.FeatureGroup(name="2010/2011", show=False)
    fg_2011, features_2011 = folium.FeatureGroup(name="2011"), []
    fg_2011_2012 = folium.FeatureGroup(name="2011/2012", show=False)
    fg_2012, features_2012 = folium.FeatureGroup(name="2012"), []
    fg_2012_2013 = folium.FeatureGroup(name="2012/2013", show=False)
    fg_2013, features_2013 = folium.FeatureGroup(name="2013"), []
    fg_2013_2014 = folium.FeatureGroup(name="2013/2014", show=False)
    fg_2014, features_2014 = folium.FeatureGroup(name="2014"), []
    fg_2014_2015 = folium.FeatureGroup(name="2014/2015", show=False)
    fg_2015, features_2015 = folium.FeatureGroup(name="2015"), []
    fg_2015_2016 = folium.FeatureGroup(name="2015/2016", show=False)
    fg_2016, features_2016 = folium.FeatureGroup(name="2016"), []
    fg_2016_2017 = folium.FeatureGroup(name="2016/2017", show=False)
    fg_2017, features_2017 = folium.FeatureGroup(name="2017"), []
    fg_2017_2018 = folium.FeatureGroup(name="2017/2018", show=False)
    fg_2018, features_2018 = folium.FeatureGroup(name="2018"), []
    fg_2018_2019 = folium.FeatureGroup(name="2018/2019", show=False)
    fg_2019, features_2019 = folium.FeatureGroup(name="2019"), []
    fg_2019_2020 = folium.FeatureGroup(name="2019/2020", show=False)
    fg_2020, features_2020 = folium.FeatureGroup(name="2020"), []
    fg_2020_2021 = folium.FeatureGroup(name="2020/2021", show=False)
    fg_2021, features_2021 = folium.FeatureGroup(name="2021"), []

    intermediary_layers = [fg_2008_2009, fg_2009_2010, fg_2010_2011, fg_2011_2012, fg_2012_2013, fg_2013_2014, fg_2014_2015, fg_2015_2016, fg_2016_2017, fg_2017_2018, fg_2018_2019, fg_2019_2020, fg_2020_2021]
    yearly_layers = [fg_2008, fg_2009, fg_2010, fg_2011, fg_2012, fg_2013, fg_2014, fg_2015, fg_2016, fg_2017, fg_2018, fg_2018, fg_2019, fg_2020, fg_2021]

    for feature in features:
        coordinates = convert_crs(feature.geometry['rings'][0])
        date = feature.attributes["CONS_DATE"]
        if date.endswith("2008"):
            features_2008.append(coordinates)
            folium.Polygon(locations=coordinates, color="#ff0000", fill=True, fill_color="#ff0000", fill_opacity=0.5).add_to(fg_2008)
        elif date.endswith("2009"):
            features_2009.append(coordinates)
            folium.Polygon(locations=coordinates, color="#ff8700", fill=True, fill_color="#ff8700", fill_opacity=0.5).add_to(fg_2009)
        elif date.endswith("2010"):
            features_2010.append(coordinates)
            folium.Polygon(locations=coordinates, color="#ffd300", fill=True, fill_color="#ffd300", fill_opacity=0.5).add_to(fg_2010)
        elif date.endswith("2011"):
            features_2011.append(coordinates)
            folium.Polygon(locations=coordinates, color="#deff0a", fill=True, fill_color="#deff0a", fill_opacity=0.5).add_to(fg_2011)
        elif date.endswith("2012"):
            features_2012.append(coordinates)
            folium.Polygon(locations=coordinates, color="#a1ff0a", fill=True, fill_color="#a1ff0a", fill_opacity=0.5).add_to(fg_2012)
        elif date.endswith("2013"):
            features_2013.append(coordinates)
            folium.Polygon(locations=coordinates, color="#0aff99", fill=True, fill_color="#0aff99", fill_opacity=0.5).add_to(fg_2013)
        elif date.endswith("2014"):
            features_2014.append(coordinates)
            folium.Polygon(locations=coordinates, color="#0aefff", fill=True, fill_color="#0aefff", fill_opacity=0.5).add_to(fg_2014)
        elif date.endswith("2015"):
            features_2015.append(coordinates)
            folium.Polygon(locations=coordinates, color="#147df5", fill=True, fill_color="#147df5", fill_opacity=0.5).add_to(fg_2015)
        elif date.endswith("2016"):
            features_2016.append(coordinates)
            folium.Polygon(locations=coordinates, color="#580aff", fill=True, fill_color="#580aff", fill_opacity=0.5).add_to(fg_2016)
        elif date.endswith("2017"):
            features_2017.append(coordinates)
            folium.Polygon(locations=coordinates, color="#be0aff", fill=True, fill_color="#be0aff", fill_opacity=0.5).add_to(fg_2017)
        elif date.endswith("2018"):
            features_2018.append(coordinates)
            folium.Polygon(locations=coordinates, color="#7b4618", fill=True, fill_color="#7b4618", fill_opacity=0.5).add_to(fg_2018)
        elif date.endswith("2019"):
            features_2019.append(coordinates)
            folium.Polygon(locations=coordinates, color="#606f49", fill=True, fill_color="#606f49", fill_opacity=0.5).add_to(fg_2019)
        elif date.endswith("2020"):
            features_2020.append(coordinates)
            folium.Polygon(locations=coordinates, color="#b4418e", fill=True, fill_color="#b4418e", fill_opacity=0.5).add_to(fg_2020)
        elif date.endswith("2021"):
            features_2021.append(coordinates)
            folium.Polygon(locations=coordinates, color="#ea515f", fill=True, fill_color="#ea515f", fill_opacity=0.5).add_to(fg_2021)

    # for i in range(len(yearly_layers)-1):
    #     layer_a = yearly_layers[i]
    #     layer_b = yearly_layers[i + 1]
    #     for f1 in layer_a:
    #         for f2 in layer_b:
    #             try:
    #                 intersection = sutherland_hodgman(f1, f2)
    #             except Exception as e:
    #                 print("An error occurred:", e)
    #             if intersection:
    #                 print("INTERSECTION!!!!!")
    #                 folium.Polygon(locations=intersection, color="yellow", fill=True, fill_color="yellow", fill_opacity=0.5).add_to(intermediary_layers[i])


    # TODO: find a way to prefilter polygons so we don't have to compare to run the whole algorithm on every pair (check if they intersect based on coords)
    # TODO: cast coordinates as polygons to ensure that they are clockwise
    for f1 in features_2008:
        for f2 in features_2009:
            intersection = None
            try:
                p1, p2 = Polygon(f1), Polygon(f2)
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
                print("An error occurred:", e)
            if intersection:
                intersection_polygon = Polygon(intersection)
                print("area: ", intersection_polygon.area)
                # if intersection_polygon.area > 0.0000001 and intersection_polygon.area < 0.0002:
                folium.Polygon(locations=intersection_polygon.exterior.coords, color="yellow", fill=True, fill_color="yellow", fill_opacity=0.5).add_to(fg_2008_2009)
                # if intersection.is_empty:
                #     continue
                # elif type(intersection) == Polygon:
                #     print("The intersection is a polygon.")
                #     print("area: ", intersection.area)
                #     #TODO: create a method to check area without calculating intersection
                #     if intersection.area > 0.0000001:
                #         if foo.within(boo):
                #             intersection = foo.exterior.coords
                #         elif boo.within(foo):
                #             intersection = boo.exterior.coords
                #         else: 
                #             intersection = sutherland_hodgman(list(foo.exterior.coords), list(boo.exterior.coords))
                #         if intersection:
                #             print("here!!!")
                #             folium.Polygon(locations=intersection, color="yellow", fill=True, fill_color="yellow", fill_opacity=0.5).add_to(fg_2008_2009)
                #     # do something with the polygon
                # elif type(intersection) == MultiPolygon:
                #     print("The intersection is a multi-polygon.")
                #     # do something with the multi-polygon
                # elif type(intersection) == GeometryCollection:
                #     print("The intersection is a geometry collection.")
                #     # do something with the geometry collection
                # else:
                #     print("Unknown geometry type returned.")
                

    fg_2008.add_to(m)
    fg_2008_2009.add_to(m)
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

    Geocoder().add_to(m)
    folium.LayerControl().add_to(m)
    m.save("data/map-time.html")

def create_zone_map(features):
    '''creates a folium map'''
    m = folium.Map(location=OTTAWA, zoom_start=13)
    fg_all_zones = folium.FeatureGroup(name="All Zones")

    for feature in features:
        coordinates = convert_crs(feature.geometry['rings'][0])
        zone = feature.attributes["PARENTZONE"]

        color = get_color(zone)
        polygon = folium.Polygon(locations=coordinates, color=color, fill=True, fill_color=color, fill_opacity=0.5)
        polygon.add_to(fg_all_zones)

    fg_all_zones.add_to(m)
    Geocoder().add_to(m)
    folium.LayerControl().add_to(m)
    m.save("data/map.html")

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
        clip_start, clip_end  = clip_edge[0], clip_edge[1] # rename
        
        for subject_edge in subject_edges:
            subject_start, subject_end = subject_edge[0], subject_edge[1] # rename
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
    # create maps 
    # create_zone_map(features)
    create_timeline_map(features)

if __name__ == "__main__":
    main()
