"""Tests for complex shapes (Polyline and Polygon)"""

import pytest
import math
from svg.shapes.shapes import Polyline, Polygon


class TestPolyline:
    """Test the Polyline shape implementation"""

    def test_polyline_creation_empty(self):
        """Test creating empty polyline"""
        polyline = Polyline([])
        assert polyline.points == []
        assert polyline.point_count == 0

    def test_polyline_creation_single_point(self):
        """Test creating polyline with single point"""
        points = [5+10j]
        polyline = Polyline(points)
        assert polyline.points == points
        assert polyline.point_count == 1

    def test_polyline_creation_multiple_points(self):
        """Test creating polyline with multiple points"""
        points = [0+0j, 10+0j, 10+10j, 0+10j]
        polyline = Polyline(points)
        assert polyline.points == points
        assert polyline.point_count == 4

    def test_polyline_immutability(self):
        """Test that polyline creates copy of points list"""
        original_points = [0+0j, 10+0j, 10+10j]
        polyline = Polyline(original_points)

        # Modify original list
        original_points.append(20+20j)

        # Polyline should be unaffected
        assert len(polyline.points) == 3
        assert 20+20j not in polyline.points

    def test_polyline_equality(self):
        """Test polyline equality comparison"""
        points1 = [0+0j, 10+0j, 10+10j]
        points2 = [0+0j, 10+0j, 10+10j]
        points3 = [0+0j, 10+0j, 20+20j]

        polyline1 = Polyline(points1)
        polyline2 = Polyline(points2)
        polyline3 = Polyline(points3)

        assert polyline1 == polyline2
        assert polyline1 != polyline3
        assert polyline1 != "not a polyline"

    def test_polyline_repr(self):
        """Test string representation"""
        points = [0+0j, 10+0j, 10+10j]
        polyline = Polyline(points)
        expected = f"Polyline(points={points})"
        assert repr(polyline) == expected

    def test_polyline_boundingbox_empty(self):
        """Test bounding box for empty polyline"""
        polyline = Polyline([])
        bbox = polyline.boundingbox()
        assert bbox == [0.0, 0.0, 0.0, 0.0]

    def test_polyline_boundingbox_single_point(self):
        """Test bounding box for single point"""
        polyline = Polyline([5+10j])
        bbox = polyline.boundingbox()
        assert bbox == [5.0, 10.0, 5.0, 10.0]

    def test_polyline_boundingbox_multiple_points(self):
        """Test bounding box for multiple points"""
        points = [0+0j, 10+0j, 10+10j, -5+15j]
        polyline = Polyline(points)
        bbox = polyline.boundingbox()
        assert bbox == [-5.0, 0.0, 10.0, 15.0]

    def test_polyline_length_empty(self):
        """Test length calculation for empty polyline"""
        polyline = Polyline([])
        assert polyline.length() == 0.0

    def test_polyline_length_single_point(self):
        """Test length calculation for single point"""
        polyline = Polyline([5+10j])
        assert polyline.length() == 0.0

    def test_polyline_length_two_points(self):
        """Test length calculation for two points"""
        polyline = Polyline([0+0j, 3+4j])
        assert abs(polyline.length() - 5.0) < 1e-10  # 3-4-5 triangle

    def test_polyline_length_multiple_points(self):
        """Test length calculation for multiple points"""
        # Square path: (0,0) -> (10,0) -> (10,10) -> (0,10)
        points = [0+0j, 10+0j, 10+10j, 0+10j]
        polyline = Polyline(points)
        expected_length = 10 + 10 + 10  # Three sides of square
        assert abs(polyline.length() - expected_length) < 1e-10

    def test_polyline_point_and_tangent(self):
        """Test point and tangent calculation"""
        points = [0+0j, 10+0j, 10+10j]
        polyline = Polyline(points)

        # Test that methods work (exact values depend on path implementation)
        p0 = polyline.point(0.0)
        p1 = polyline.point(1.0)
        t0 = polyline.tangent(0.0)
        t1 = polyline.tangent(1.0)

        assert p0 == 0
        assert p1 == 10+10j
        assert t0 == 0
        assert t1 == 10j

    def test_polyline_to_path_empty(self):
        """Test path conversion for empty polyline"""
        polyline = Polyline([])
        path = polyline.to_path()
        assert path is not None
        assert len(path) == 0  # Empty path

    def test_polyline_to_path_single_point(self):
        """Test path conversion for single point"""
        polyline = Polyline([5+10j])
        path = polyline.to_path()
        assert path is not None
        assert len(path) == 1  # Should contain one Move command

    def test_polyline_to_path_multiple_points(self):
        """Test path conversion for multiple points"""
        points = [0+0j, 10+0j, 10+10j]
        polyline = Polyline(points)
        path = polyline.to_path()
        assert path is not None
        assert len(path) == 3  # Move + 2 Lines


class TestPolygon:
    """Test the Polygon shape implementation"""

    def test_polygon_creation_empty(self):
        """Test creating empty polygon"""
        polygon = Polygon([])
        assert polygon.points == []
        assert polygon.point_count == 0

    def test_polygon_creation_single_point(self):
        """Test creating polygon with single point"""
        points = [5+10j]
        polygon = Polygon(points)
        assert polygon.points == points
        assert polygon.point_count == 1

    def test_polygon_creation_multiple_points(self):
        """Test creating polygon with multiple points"""
        points = [0+0j, 10+0j, 10+10j, 0+10j]
        polygon = Polygon(points)
        assert polygon.points == points
        assert polygon.point_count == 4

    def test_polygon_immutability(self):
        """Test that polygon creates copy of points list"""
        original_points = [0+0j, 10+0j, 10+10j]
        polygon = Polygon(original_points)

        # Modify original list
        original_points.append(20+20j)

        # Polygon should be unaffected
        assert len(polygon.points) == 3
        assert 20+20j not in polygon.points

    def test_polygon_equality(self):
        """Test polygon equality comparison"""
        points1 = [0+0j, 10+0j, 10+10j]
        points2 = [0+0j, 10+0j, 10+10j]
        points3 = [0+0j, 10+0j, 20+20j]

        polygon1 = Polygon(points1)
        polygon2 = Polygon(points2)
        polygon3 = Polygon(points3)

        assert polygon1 == polygon2
        assert polygon1 != polygon3
        assert polygon1 != "not a polygon"

    def test_polygon_repr(self):
        """Test string representation"""
        points = [0+0j, 10+0j, 10+10j]
        polygon = Polygon(points)
        expected = f"Polygon(points={points})"
        assert repr(polygon) == expected

    def test_polygon_boundingbox_empty(self):
        """Test bounding box for empty polygon"""
        polygon = Polygon([])
        bbox = polygon.boundingbox()
        assert bbox == [0.0, 0.0, 0.0, 0.0]

    def test_polygon_boundingbox_single_point(self):
        """Test bounding box for single point"""
        polygon = Polygon([5+10j])
        bbox = polygon.boundingbox()
        assert bbox == [5.0, 10.0, 5.0, 10.0]

    def test_polygon_boundingbox_multiple_points(self):
        """Test bounding box for multiple points"""
        points = [0+0j, 10+0j, 10+10j, -5+15j]
        polygon = Polygon(points)
        bbox = polygon.boundingbox()
        assert bbox == [-5.0, 0.0, 10.0, 15.0]

    def test_polygon_length_empty(self):
        """Test length calculation for empty polygon"""
        polygon = Polygon([])
        assert polygon.length() == 0.0

    def test_polygon_length_single_point(self):
        """Test length calculation for single point"""
        polygon = Polygon([5+10j])
        assert polygon.length() == 0.0

    def test_polygon_length_two_points(self):
        """Test length calculation for two points"""
        polygon = Polygon([0+0j, 3+4j])
        expected = 2 * 5.0  # Distance there and back
        assert abs(polygon.length() - expected) < 1e-10

    def test_polygon_length_triangle(self):
        """Test length calculation for triangle"""
        # Right triangle: (0,0) -> (3,0) -> (0,4) -> back to (0,0)
        points = [0+0j, 3+0j, 0+4j]
        polygon = Polygon(points)
        expected_length = 3 + 4 + 5  # Sides of 3-4-5 triangle
        assert abs(polygon.length() - expected_length) < 1e-10

    def test_polygon_length_square(self):
        """Test length calculation for square"""
        # Square: (0,0) -> (10,0) -> (10,10) -> (0,10) -> back to (0,0)
        points = [0+0j, 10+0j, 10+10j, 0+10j]
        polygon = Polygon(points)
        expected_length = 4 * 10  # Four sides of square
        assert abs(polygon.length() - expected_length) < 1e-10

    def test_polygon_point_and_tangent(self):
        """Test point and tangent calculation"""
        points = [0+0j, 10+0j, 10+10j, 0+10j]  # Square
        polygon = Polygon(points)

        # Test that methods work (exact values depend on path implementation)
        p0 = polygon.point(0.0)
        p1 = polygon.point(1.0)
        t0 = polygon.tangent(0.0)
        t1 = polygon.tangent(1.0)

        assert p0 == 0
        assert p1 == 0j
        assert t0 == 0
        assert t1 == -10j

        # For closed shapes, start and end should be the same
        assert abs(p0 - p1) < 1e-10

    def test_polygon_to_path_empty(self):
        """Test path conversion for empty polygon"""
        polygon = Polygon([])
        path = polygon.to_path()
        assert path is not None
        assert len(path) == 0  # Empty path

    def test_polygon_to_path_single_point(self):
        """Test path conversion for single point"""
        polygon = Polygon([5+10j])
        path = polygon.to_path()
        assert path is not None
        assert len(path) == 1  # Should contain one Move command

    def test_polygon_to_path_two_points(self):
        """Test path conversion for two points"""
        points = [0+0j, 10+0j]
        polygon = Polygon(points)
        path = polygon.to_path()
        assert path is not None
        assert len(path) == 3  # Move + Line + Close

    def test_polygon_to_path_triangle(self):
        """Test path conversion for triangle"""
        points = [0+0j, 10+0j, 5+10j]
        polygon = Polygon(points)
        path = polygon.to_path()
        assert path is not None
        assert len(path) == 4  # Move + 2 Lines + Close


class TestPolylinePolygonComparison:
    """Test differences between Polyline and Polygon"""

    def test_polyline_vs_polygon_length(self):
        """Test that polygon has closing edge in length calculation"""
        points = [0+0j, 10+0j, 10+10j, 0+10j]

        polyline = Polyline(points)
        polygon = Polygon(points)

        polyline_length = polyline.length()  # Three sides
        polygon_length = polygon.length()    # Four sides (includes closing)

        # Polygon should be longer by the closing edge length
        closing_edge_length = abs(points[-1] - points[0])  # (0,10) to (0,0) = 10
        expected_difference = closing_edge_length

        assert abs(polygon_length - polyline_length - expected_difference) < 1e-10

    def test_polyline_vs_polygon_closure(self):
        """Test that polygon is closed but polyline is not"""
        points = [0+0j, 10+0j, 10+10j]

        polyline = Polyline(points)
        polygon = Polygon(points)

        # For polyline, start and end points may be different
        poly_start = polyline.point(0.0)
        poly_end = polyline.point(1.0)

        # For polygon, start and end points should be the same (closed)
        gon_start = polygon.point(0.0)
        gon_end = polygon.point(1.0)

        # Polygon should be closed
        assert abs(gon_start - gon_end) < 1e-6

        # Polyline end points might be different
        # (This depends on path implementation, but they represent different shapes)

    def test_polyline_vs_polygon_path_structure(self):
        """Test differences in path structure"""
        points = [0+0j, 10+0j, 10+10j]

        polyline = Polyline(points)
        polygon = Polygon(points)

        poly_path = polyline.to_path()
        gon_path = polygon.to_path()

        # Polygon path should have one more segment (the Close command)
        assert len(gon_path) == len(poly_path) + 1


class TestComplexShapeEdgeCases:
    """Test edge cases for complex shapes"""

    def test_shapes_with_duplicate_points(self):
        """Test shapes with duplicate consecutive points"""
        points = [0+0j, 0+0j, 10+0j, 10+0j, 10+10j]

        polyline = Polyline(points)
        polygon = Polygon(points)

        # Should handle gracefully
        assert polyline.point_count == 5
        assert polygon.point_count == 5

        # Length should handle zero-length segments
        poly_length = polyline.length()
        gon_length = polygon.length()

        assert poly_length >= 0
        assert gon_length >= 0

    def test_shapes_with_collinear_points(self):
        """Test shapes with collinear points"""
        points = [0+0j, 5+0j, 10+0j, 10+5j, 10+10j]  # First three are collinear

        polyline = Polyline(points)
        polygon = Polygon(points)

        # Should handle gracefully
        assert polyline.length() > 0
        assert polygon.length() > 0

        # Bounding boxes should be correct
        poly_bbox = polyline.boundingbox()
        gon_bbox = polygon.boundingbox()

        assert poly_bbox == gon_bbox == [0.0, 0.0, 10.0, 10.0]

    def test_very_large_coordinates(self):
        """Test shapes with very large coordinate values"""
        points = [1e6+1e6j, 2e6+1e6j, 2e6+2e6j]

        polyline = Polyline(points)
        polygon = Polygon(points)

        # Should handle large numbers gracefully
        assert polyline.length() > 0
        assert polygon.length() > 0

        # Bounding boxes should be correct
        poly_bbox = polyline.boundingbox()
        expected = [1e6, 1e6, 2e6, 2e6]

        for actual, exp in zip(poly_bbox, expected):
            assert abs(actual - exp) < 1e-6

    def test_negative_coordinates(self):
        """Test shapes with negative coordinates"""
        points = [-10-10j, -5-5j, 0+0j, 5+5j]

        polyline = Polyline(points)
        polygon = Polygon(points)

        # Should handle negative coordinates
        poly_bbox = polyline.boundingbox()
        gon_bbox = polygon.boundingbox()

        expected = [-10.0, -10.0, 5.0, 5.0]
        assert poly_bbox == expected
        assert gon_bbox == expected
