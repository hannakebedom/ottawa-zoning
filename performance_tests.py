import unittest
import time
from shapely.geometry import Polygon
from sutherland import SutherlandHodgman

class PerformanceTests(unittest.TestCase):
    def test_performance_non_intersecting(self):
        p1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
        p2 = Polygon([(2, 2), (2, 3), (3, 3), (3, 2), (2, 2)])
        vertices_p1 = p1.exterior.coords
        vertices_p2 = p2.exterior.coords
        
        start_time_sutherland = time.time()
        SutherlandHodgman().run(vertices_p1, vertices_p2)
        end_time_sutherland = time.time()

        start_time_intersection = time.time()
        p1.intersection(p2)
        end_time_intersection = time.time()

        time_taken_sutherland = end_time_sutherland - start_time_sutherland
        time_taken_intersection = end_time_intersection - start_time_intersection
        self.assertLess(time_taken_sutherland, time_taken_intersection)
    
    def test_performance_fuly_overlapping(self):
        p1 = Polygon([(0, 0), (0, 3), (3, 3), (3, 0), (0, 0)])
        p2 = Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
        vertices_p1 = p1.exterior.coords
        vertices_p2 = p2.exterior.coords
        
        start_time_sutherland = time.time()
        SutherlandHodgman().run(vertices_p1, vertices_p2)
        end_time_sutherland = time.time()

        start_time_intersection = time.time()
        p1.intersection(p2)
        end_time_intersection = time.time()

        time_taken_sutherland = end_time_sutherland - start_time_sutherland
        time_taken_intersection = end_time_intersection - start_time_intersection
        self.assertLess(time_taken_sutherland, time_taken_intersection)

    def test_performance_partially_overlapping(self):
        p1 = Polygon([(0, 0), (0, 3), (3, 3), (3, 0), (0, 0)])
        p2 = Polygon([(2, 1), (2, 4), (4, 4), (4, 1), (2, 1)])
        vertices_p1 = p1.exterior.coords
        vertices_p2 = p2.exterior.coords
        
        start_time_sutherland = time.time()
        SutherlandHodgman().run(vertices_p1, vertices_p2)
        end_time_sutherland = time.time()

        start_time_intersection = time.time()
        p1.intersection(p2)
        end_time_intersection = time.time()

        time_taken_sutherland = end_time_sutherland - start_time_sutherland
        time_taken_intersection = end_time_intersection - start_time_intersection
        self.assertLess(time_taken_sutherland, time_taken_intersection)
    
    def test_performance_concave_convex(self):
        p1 = Polygon([(0, 0), (0, 3), (3, 3), (1, 2), (3, 0), (0, 0)])
        p2 = Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
        vertices_p1 = p1.exterior.coords
        vertices_p2 = p2.exterior.coords
        
        start_time_sutherland = time.time()
        SutherlandHodgman().run(vertices_p1, vertices_p2)
        end_time_sutherland = time.time()

        start_time_intersection = time.time()
        p1.intersection(p2)
        end_time_intersection = time.time()

        time_taken_sutherland = end_time_sutherland - start_time_sutherland
        time_taken_intersection = end_time_intersection - start_time_intersection
        self.assertLess(time_taken_sutherland, time_taken_intersection)
        

if __name__ == '__main__':
    unittest.main()



