# import shapely
import folium
from folium.plugins import Geocoder
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
import matplotlib.pyplot as plt

OTTAWA = [45.4215, -75.6972]

def create_test_map():
    coords_1 = [[45.41560770492214, -75.67968677643513],
        [45.423823130398006, -75.67968677643513],
        [45.423823130398006, -75.69377985257785],
        [45.41560770492214, -75.69377985257785],
        [45.41560770492214, -75.67968677643513]
    ]

    coords_2 = [[45.42650545942101, -75.6927447678894],
        [45.41991117211023, -75.68709161305293],
        [45.4264495788662, -75.6804829954265],
        [45.42650545942101, -75.6927447678894]
    ]

    m = folium.Map(location=OTTAWA, zoom_start=13)
    polygon_1 = folium.Polygon(locations=coords_1, color="red", fill=True, fill_color="red", fill_opacity=0.5)
    polygon_2 = folium.Polygon(locations=coords_2, color="blue", fill=True, fill_color="blue", fill_opacity=0.5)
    poly1 = Polygon(polygon_1.locations)
    poly2 = Polygon(polygon_2.locations)

    intersection = sutherland_hodgman(poly1.exterior.coords, poly2.exterior.coords)
    intersection_polygon = folium.Polygon(locations=intersection, color="yellow", fill=True, fill_color="yellow", fill_opacity=0.5)
  
    plt.plot(*poly1.exterior.xy)
    plt.plot(*poly2.exterior.xy)
    plt.plot(*Polygon(intersection).exterior.xy)
    plt.show()

    polygon_1.add_to(m)
    polygon_2.add_to(m)
    intersection_polygon.add_to(m)
    Geocoder().add_to(m)
    m.save("data/map-sutherland-hodgman.html")

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
    create_test_map()

if __name__ == "__main__":
    main()

