from shapely.geometry import Polygon

class SutherlandHodgman:
    def same_side(self, edge_start, edge_end, p):
        '''given an edge and a point determine if the point lies on the same side as the rest of the polygon'''
        return (edge_end[0] - edge_start[0]) * (p[1] - edge_start[1]) <= (edge_end[1] - edge_end[1]) * (p[0] - edge_start[0])

    def intersection(self, p1, p2, p3, p4):
        '''find the intersection point between two lines that intersect'''
        x = ( (p1[0]*p2[1]-p1[1]*p2[0])*(p3[0]-p4[0])-(p1[0]-p2[0])*(p3[0]*p4[1]-p3[1]*p4[0]) ) / ( (p1[0]-p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]-p4[0]) )
        y = ( (p1[0]*p2[1]-p1[1]*p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]*p4[1]-p3[1]*p4[0]) ) / ( (p1[0]-p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]-p4[0]) )
        return (x, y)

    def run(self, subject_polygon, clipping_polygon):
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
                if self.same_side(clip_start, clip_end, subject_end):
                    if not self.same_side(clip_start, clip_end, subject_start):
                        intersection_point = self.intersection(clip_start, clip_end, subject_start, subject_end)
                        output_polygon.append(intersection_point)
                    output_polygon.append(tuple(subject_end))
                elif self.same_side(clip_start, clip_end,subject_start):
                    intersection_point = self.intersection(clip_start, clip_end, subject_start, subject_end)
                    output_polygon.append(intersection_point)
        
        return output_polygon
