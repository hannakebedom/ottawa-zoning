import unittest
from shapely.geometry import Polygon
from sutherland import SutherlandHodgman

class CorrectnessTests(unittest.TestCase):
    def test_non_intersecting(self):
        p1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
        p2 = Polygon([(2, 2), (2, 3), (3, 3), (3, 2), (2, 2)])
        expected = []
        actual = SutherlandHodgman().run(p1.exterior.coords, p2.exterior.coords)
        self.assertEqual(expected, actual)
    
    def test_fully_overlapping(self):
        p1 = Polygon([(0, 0), (0, 3), (3, 3), (3, 0), (0, 0)])
        p2 = Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
        expected = [(-0.0, 1.0), (0.0, 2.0), (3.0, 2.0), (3.0, 1.0)]
        actual = SutherlandHodgman().run(p1.exterior.coords, p2.exterior.coords)
        self.assertEqual(expected, actual)

    def test_partially_overlapping(self):
        p1 = Polygon([(0, 0), (0, 3), (3, 3), (3, 0), (0, 0)])
        p2 = Polygon([(2, 1), (2, 4), (4, 4), (4, 1), (2, 1)])
        expected = [(-0.0, 1.0), (0.0, 3.0), (3.0, 3.0), (3.0, 1.0)]
        actual = SutherlandHodgman().run(p1.exterior.coords, p2.exterior.coords)
        self.assertEqual(expected, actual)

    def test_concave_convex(self):
        p1 = Polygon([(0, 0), (0, 3), (3, 3), (1, 2), (3, 0), (0, 0)])
        p2 = Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
        expected = [(2.0, 1.0), (-0.0, 1.0), (0.0, 2.0), (1.0, 2.0)]
        actual = SutherlandHodgman().run(p1.exterior.coords, p2.exterior.coords)
        self.assertEqual(expected, actual)
    
    def test_complex(self):
        p1 = Polygon([(0, 0), (0, 3), (3, 3), (1, 2), (2, 3), (3, 2), (2, 0), (0, 0)])
        p2 = Polygon([(1, 1), (1, 3), (3, 3), (3, 2), (2, 1), (1, 1)])
        expected = [(3.0, 2.0), (3.0, 2.0), (2.0, 1.0), (-0.0, 1.0), (0.0, 3.0), (3.0, 3.0), (1.0, 2.0), (2.0, 3.0)]
        actual = SutherlandHodgman().run(p1.exterior.coords, p2.exterior.coords)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()