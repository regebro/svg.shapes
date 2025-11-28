"""Tests for Polygon shape"""

import pytest
import math
from svg.shapes.shapes import Polygon


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

        # Test specific points along the polygon perimeter
        p0 = polygon.point(0.0)  # Should be at start point (0, 0)
        p1 = polygon.point(1.0)  # Should be back at start for closed shape

        # Verify that polygon is closed (start == end)
        assert abs(p0 - p1) < 1e-10

        # Test tangent vectors
        t0 = polygon.tangent(0.0)  # Should point along first segment
        t1 = polygon.tangent(1.0)  # Should point along first segment (closed)

        # Tangent vectors should have non-zero magnitude
        assert abs(t0) > 0
        assert abs(t1) > 0

        # Since it's closed, start and end tangents should be the same
        assert abs(t0 - t1) < 1e-6

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

    def test_polygon_closed_shape(self):
        """Test that polygon is properly closed"""
        points = [0+0j, 10+0j, 10+10j, 0+10j]
        polygon = Polygon(points)

        start_point = polygon.point(0.0)
        end_point = polygon.point(1.0)
        distance = abs(end_point - start_point)
        assert distance < 1e-6, "Polygon not properly closed"

    def test_polygon_with_duplicate_points(self):
        """Test polygon with duplicate consecutive points"""
        points = [0+0j, 0+0j, 10+0j, 10+0j, 10+10j]

        polygon = Polygon(points)

        # Should handle gracefully
        assert polygon.point_count == 5

        # Length should handle zero-length segments
        length = polygon.length()
        assert length >= 0

    def test_polygon_with_collinear_points(self):
        """Test polygon with collinear points"""
        points = [0+0j, 5+0j, 10+0j, 10+5j, 10+10j]  # First three are collinear

        polygon = Polygon(points)

        # Should handle gracefully
        assert polygon.length() > 0

        # Bounding box should be correct
        bbox = polygon.boundingbox()
        assert bbox == [0.0, 0.0, 10.0, 10.0]

    def test_polygon_very_large_coordinates(self):
        """Test polygon with very large coordinate values"""
        points = [1e6+1e6j, 2e6+1e6j, 2e6+2e6j]

        polygon = Polygon(points)

        # Should handle large numbers gracefully
        assert polygon.length() > 0

        # Bounding box should be correct
        bbox = polygon.boundingbox()
        expected = [1e6, 1e6, 2e6, 2e6]

        for actual, exp in zip(bbox, expected):
            assert abs(actual - exp) < 1e-6

    def test_polygon_negative_coordinates(self):
        """Test polygon with negative coordinates"""
        points = [-10-10j, -5-5j, 0+0j, 5+5j]

        polygon = Polygon(points)

        # Should handle negative coordinates
        bbox = polygon.boundingbox()

        expected = [-10.0, -10.0, 5.0, 5.0]
        assert bbox == expected

    def test_polygon_complex_patterns(self):
        """Test polygon with complex coordinate patterns"""
        base_point = 100 + 200j
        offset = 50 + 75j

        complex_points = [
            base_point,
            base_point + offset,
            base_point + offset + 1j * offset.real,
            base_point + 1j * offset.imag
        ]

        polygon = Polygon(complex_points)

        # Should handle complex coordinates without issues
        bbox = polygon.boundingbox()
        length = polygon.length()

        # Basic sanity checks
        assert len(bbox) == 4
        assert length >= 0

    def test_polygon_regular_shapes(self):
        """Test regular polygon shapes"""
        # Equilateral triangle
        side = 10
        height = side * math.sqrt(3) / 2
        triangle_points = [
            0+0j,
            side+0j,
            side/2 + height*1j
        ]
        triangle = Polygon(triangle_points)

        # Should have perimeter close to 3 * side
        expected_perimeter = 3 * side
        assert abs(triangle.length() - expected_perimeter) < 1e-6

        # Square
        square_points = [0+0j, 10+0j, 10+10j, 0+10j]
        square = Polygon(square_points)
        assert square.length() == 40  # 4 * 10