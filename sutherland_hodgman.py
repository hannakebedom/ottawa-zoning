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
    poly1 = [(45.312958358415, -75.61457877607015), (45.31412054253117, -75.6152245623515), (45.31443568107559, -75.61430681021956), (45.31333923850835, -75.61363926853866), (45.312958358415, -75.61457877607015)]
    poly1 = Polygon(poly1)
    poly2 = [(45.31442932165754, -75.61110690607464), (45.31429743258645, -75.611070721935), (45.31414337452337, -75.61102845620088), (45.31417111743773, -75.61068863790193), (45.314085597430115, -75.61053731220076), (45.31389503070981, -75.61050746477713), (45.313671083387874, -75.61047238915853), (45.31356943294744, -75.61038975313555), (45.31345173915861, -75.61029407357465), (45.3133696925321, -75.61016703472548), (45.313292009723, -75.61002588873309), (45.311618706779214, -75.61182322986872), (45.31092422237341, -75.6133929289282), (45.31162248711553, -75.61378923958041), (45.31127247074567, -75.61475533544765), (45.31052125007903, -75.61432739152104), (45.3096591389172, -75.61634807090428), (45.31034616705967, -75.6168935980134), (45.31005441052384, -75.61774772427036), (45.31046229486312, -75.61798417253127), (45.312220983067576, -75.61901710036071), (45.31323514460108, -75.61964584110953), (45.31381522605431, -75.61995267866112), (45.313875119670406, -75.6198055822283), (45.313928273456554, -75.61967507049224), (45.31451550823056, -75.61823322325725), (45.315481962713896, -75.61585725209429), (45.31611715009543, -75.61431275167685), (45.31640985895859, -75.61361061946764), (45.316988942075525, -75.61218782549983), (45.31700894677298, -75.61213867328074), (45.31700229896562, -75.6121043459588), (45.316951091114404, -75.61179881006605), (45.31683144171079, -75.61176598113398), (45.316639674547815, -75.61171336321453), (45.3163898054097, -75.61164480469036), (45.31621605127533, -75.61159712930159), (45.31594956991897, -75.61152401272567), (45.31562482853849, -75.6114349124259), (45.315403783126676, -75.61137426446614), (45.315278543070434, -75.61133990300819), (45.31503930769817, -75.61127426490701), (45.31478576824377, -75.61120470206636), (45.31450060306828, -75.61112646419501), (45.31442932165754, -75.61110690607464)]
    poly2 = Polygon(poly2)
    poly_intersect = []
    print("intersects? ", poly1.intersects(poly2))
    print("touches? ", poly1.touches(poly2))

    intersection = sutherland_hodgman(poly2.exterior.coords, poly1.exterior.coords, )
    print("intersection", intersection)
    # sutherland_hodgman(poly1.exterior.coords, poly2.exterior.coords)
    # for geom in intersection.geoms:
    #     if geom.geom_type == "Polygon":
    #         poly_intersect = geom

    # intersection_polygon = folium.Polygon(locations=intersection.exterior.coords, color="yellow", fill=True, fill_color="yellow", fill_opacity=0.5)
    
    # print("significant intersection? ", intersection.area > 0.1)
    plt.plot(*poly1.exterior.xy)
    plt.plot(*poly2.exterior.xy)
    plt.plot(*Polygon(intersection).exterior.xy)
    plt.show()

    polygon_1.add_to(m)
    polygon_2.add_to(m)
    # intersection_polygon.add_to(m)
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

