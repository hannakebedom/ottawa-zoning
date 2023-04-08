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

    intersection = clip(polygon_1.locations, polygon_2.locations)
    # intersection_polygon = folium.Polygon(locations=intersection.exterior.coords, color="yellow", fill=True, fill_color="yellow", fill_opacity=0.5)
  
    plt.plot(*poly1.exterior.xy)
    plt.plot(*poly2.exterior.xy)
    plt.plot(*Polygon(intersection).exterior.xy)
    plt.show()

    # polygon_1.add_to(m)
    # polygon_2.add_to(m)
    # intersection_polygon.add_to(m)
    Geocoder().add_to(m)
    m.save("data/map-sutherland-hodgman.html")

def is_inside(p1,p2,q):
    R = (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])
    if R <= 0:
        return True
    else:
        return False

def compute_intersection(p1,p2,p3,p4):
    
    """
    given points p1 and p2 on line L1, compute the equation of L1 in the
    format of y = m1 * x + b1. Also, given points p3 and p4 on line L2,
    compute the equation of L2 in the format of y = m2 * x + b2.
    
    To compute the point of intersection of the two lines, equate
    the two line equations together
    
    m1 * x + b1 = m2 * x + b2
    
    and solve for x. Once x is obtained, substitute it into one of the
    equations to obtain the value of y.
    
    if one of the lines is vertical, then the x-coordinate of the point of
    intersection will be the x-coordinate of the vertical line. Note that
    there is no need to check if both lines are vertical (parallel), since
    this function is only called if we know that the lines intersect.
    """
    
    # if first line is vertical
    if p2[0] - p1[0] == 0:
        x = p1[0]
        
        # slope and intercept of second line
        m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
        b2 = p3[1] - m2 * p3[0]
        
        # y-coordinate of intersection
        y = m2 * x + b2
    
    # if second line is vertical
    elif p4[0] - p3[0] == 0:
        x = p3[0]
        
        # slope and intercept of first line
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b1 = p1[1] - m1 * p1[0]
        
        # y-coordinate of intersection
        y = m1 * x + b1
    
    # if neither line is vertical
    else:
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b1 = p1[1] - m1 * p1[0]
        
        # slope and intercept of second line
        m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
        b2 = p3[1] - m2 * p3[0]
    
        # x-coordinate of intersection
        x = (b2 - b1) / (m1 - m2)
    
        # y-coordinate of intersection
        y = m1 * x + b1
    
    intersection = (x,y)
    
    return intersection

def clip(subject_polygon,clipping_polygon):
    
    final_polygon = subject_polygon.copy()
    
    for i in range(len(clipping_polygon)):
        
        # stores the vertices of the next iteration of the clipping procedure
        next_polygon = final_polygon.copy()
        
        # stores the vertices of the final clipped polygon
        final_polygon = []
        
        # these two vertices define a line segment (edge) in the clipping
        # polygon. It is assumed that indices wrap around, such that if
        # i = 1, then i - 1 = K.
        c_edge_start = clipping_polygon[i - 1]
        c_edge_end = clipping_polygon[i]

        print("clip edge")
        print((c_edge_start, c_edge_end))
        
        for j in range(len(next_polygon)):
            
            # these two vertices define a line segment (edge) in the subject
            # polygon
            s_edge_start = next_polygon[j - 1]
            s_edge_end = next_polygon[j]
            
            if is_inside(c_edge_start,c_edge_end,s_edge_end):
                if not is_inside(c_edge_start,c_edge_end,s_edge_start):
                    intersection = compute_intersection(s_edge_start,s_edge_end,c_edge_start,c_edge_end)
                    final_polygon.append(intersection)
                final_polygon.append(tuple(s_edge_end))
            elif is_inside(c_edge_start,c_edge_end,s_edge_start):
                intersection = compute_intersection(s_edge_start,s_edge_end,c_edge_start,c_edge_end)
                final_polygon.append(intersection)
    
    return final_polygon

def sutherland_hodgman(sub, clip):
    sub_vertices, clip_vertices = list(sub.exterior.coords), list(clip.exterior.coords)
    sub_edges = [LineString(sub_vertices[i:i+2]) for i in range(len(sub_vertices)-1)]
    clip_edges = [LineString(clip_vertices[i:i+2]) for i in range(len(clip_vertices)-1)]


    resulting_polygon = Polygon(sub)
    for clip_edge in clip_edges:
        next_polygon = Polygon(resulting_polygon)
        next_polygon_vertices = next_polygon.exterior.coords
        next_polygon_edges = [LineString(next_polygon_vertices[i:i+2]) for i in range(len(next_polygon_vertices)-1)]
        
        clip_edge_start = clip_edge.coords[0]
        clip_edge_end = clip_edge.coords[-1]

        final_polygon = []

        print("clip edge")
        print((clip_edge_start, clip_edge_end))

        for next_polygon_edge in next_polygon_edges:
            sub_edge_start = next_polygon_edge.coords[0]
            sub_edge_end = next_polygon_edge.coords[-1]

            if is_inside(clip_edge_start, clip_edge_end, sub_edge_end):
                if not is_inside(clip_edge_start, clip_edge_end, sub_edge_start):
                    intersection = compute_intersection(sub_edge_start, sub_edge_end, clip_edge_start, clip_edge_end)
                    final_polygon.append(intersection)
                final_polygon.append(tuple(sub_edge_end))
            elif is_inside(clip_edge_start, clip_edge_end, sub_edge_start):
                intersection = compute_intersection(sub_edge_start, sub_edge_end, clip_edge_start, clip_edge_end)
                final_polygon.append(intersection)
    
    return Polygon(final_polygon)



def line_segment_intersections(line1, line2):
    """Find the intersection points between line segment `line1` and line segment `line2`."""
    intersection = line1.intersection(line2)
    
    if intersection.geom_type == 'Point':
        return [intersection]

    return []

def intersection_points(poly1, poly_edges1, poly_edges2):
    """Find intersections points between edges of `poly1` and `poly_edges2`."""
    intersections = []
    for edge in poly_edges2:
        for index in range(len(poly_edges1)):
            intersection_pts = line_segment_intersections(edge, poly_edges1[index])
            if intersection_pts:
                intersections.extend(intersection_pts)
    
    if intersections:
        # Sort intersection points along `poly1` boundary
        intersections = sorted(intersections, key=lambda pt: poly1.exterior.project(pt))
    
    return intersections

def classify_intersection_points(poly1, poly2, intersection_pts):
    """Classify intersection points as entering or exiting."""
    entry_exit_points = []
    
    for pt in intersection_pts:
        # Extend a line segment from the intersection point to the centroid of the polygon
        pt_to_centroid = LineString([pt, poly1.centroid])
        
        # Count the intersections between the line and the other polygon
        intersections_count = pt_to_centroid.intersection(poly2.boundary).type.count('Point') - 1

        # Classify the point as 'entry' or 'exit' based on the number of intersections
        status = 'entry' if intersections_count % 2 == 1 else 'exit'
        entry_exit_points.append((pt, status))

    return entry_exit_points

# def weiler_atherton(poly1, poly2):
#     """Find the intersection of two polygons using Weiler-Atherton algorithm."""
#     poly_edges1 = [LineString(poly1.exterior.coords[i:i+2]) for i in range(len(poly1.exterior.coords)-1)]
#     poly_edges2 = [LineString(poly2.exterior.coords[i:i+2]) for i in range(len(poly2.exterior.coords)-1)]

#     intersections_poly1 = intersection_points(poly1, poly_edges1, poly_edges2)
#     intersections_poly2 = intersection_points(poly2, poly_edges2, poly_edges1)
    
#     if not intersections_poly1 or not intersections_poly2:
#         # If no intersections exist, return None
#         return None

#     entry_exit_poly1 = classify_intersection_points(poly1, poly2, intersections_poly1)
#     entry_exit_poly2 = classify_intersection_points(poly2, poly1, intersections_poly2)

#     intersection_polygons = []

#     while entry_exit_poly1:
#         _, entry_pt, exit_pt = next(
#             pt for pt in zip(entry_exit_poly1, entry_exit_poly1[1:]) if pt[0][1] == 'entry'
#         ), *(entry_exit_poly1.pop(0) for _ in range(2))

#         intersection_polygon = [entry_pt]
        
#         while entry_pt != exit_pt:
#             intersection_polygon.append(exit_pt)
#             entry_pt, entry_status = entry_exit_poly2.pop(entry_exit_poly2.index((exit_pt, 'exit')))

#             if entry_status == 'entry':
#                 poly1, poly2 = poly2, poly1
#                 entry_exit_poly1, entry_exit_poly2 = entry_exit_poly2, entry_exit_poly1
#             else:
#                 exit_pt, _ = entry_exit_poly1.pop(0)
    
#         intersection_polygons.append(Polygon(intersection_polygon))

#     return unary_union(intersection_polygons)

# # Test example
# polygon1 = Polygon([(0, 0), (5, 0), (5, 5), (0, 5)])
# polygon2 = Polygon([(2, 2), (7, 2), (7, 7), (2, 7)])

# intersection = weiler_atherton(polygon1, polygon2)
# print(intersection)

# def weiler_atherton(p1, p2): 
#     '''compute the intersection between two polygons'''

#     # convert polygons of type folium.Polygon to shapely.geometry.Polygon
#     p1 = Polygon(p1.locations)
#     p2 = Polygon(p2.locations)
#     p1_vertices = p1.exterior.coords
#     p2_vertices = p2.exterior.coords

#     # find intersection points 
#     p1_intersection_points = intersection_points(p1_vertices, p2_vertices)
#     p2_intersection_points = intersection_points(p2_vertices, p1_vertices)

#     # categorize each intersection point as either 'entry' or 'exit'
#     categorized_points_p1 = sorted(categorize_intersection_points(p1, p2, p1_intersection_points), key=lambda x: (x[0].x, x[0].y))
#     categorized_points_p2 = sorted(categorize_intersection_points(p2, p1, p2_intersection_points), key=lambda x: (x[0].x, x[0].y))

#     if not categorized_points_p1 or not categorized_points_p2:
#         return unary_union([p1, p2])
    
#     intersection_polygons = []

#     while categorized_points_p1:
#         _, entry_point, exit_point = next(point for point in zip(p1_intersection_points, p2_intersection_points[1:])), \
#                                         *(categorized_points_p1.pop(0) for _ in range(2))
#         intersection_polygon = [entry_point]

#         while entry_point != exit_point:
#             intersection_polygon.append(exit_point)
#             index = categorized_points_p2.index((exit_point[0], 'exit'))
#             entry_point, entry_status = categorized_points_p2.pop(index)
            
#             if entry_status == 'entry':
#                 p1, p2 = p2, p1
#                 categorized_points_p1, categorized_points_p2 = categorized_points_p2, categorized_points_p1
#             else:
#                 exit_point, _ = categorized_points_p2.pop(0)
        
#         intersection_polygons.append(Polygon(intersection_points))
    
#     return intersection_polygons



    # 2. check if any of the vertices are inside the other polygons, if they are mark as an entry point (point in polygon algorithm)
    # entry_points = []
    # for vertex in vertices_polygon1: 
    #     vertex = Point(vertex)
    #     if polygon2.contains(vertex):
    #         print("p1")
    #         print(vertex.x)
    #         print(vertex.y)
    #         entry_points.append(vertex)
    # for vertex in vertices_polygon2: 
    #     vertex = Point(vertex)
    #     if polygon1.contains(vertex):
    #         print(vertex.x)
    #         print(vertex.y)
    #         entry_points.append(vertex)
    
    # 3. determine intersection points between the edges of the polygons

    # print("edges")
    # print(edges_polygon1)
    # print(edges_polygon2)
    
def main():
    create_test_map()

if __name__ == "__main__":
    main()

