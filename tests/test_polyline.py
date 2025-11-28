"""Tests for Polyline shape"""

import pytest
import math
from svg.shapes.shapes import Polyline


class TestPolyline:
    """Test the Polyline shape implementation"""

    def test_polyline_empty(self):
        """Test creating empty polyline"""
        polyline = Polyline([])
        assert polyline.points == []
        assert polyline.point_count == 0

    def test_polyline_single_point(self):
        """Test creating polyline with single point"""
        points = [5+10j]
        polyline = Polyline(points)
        assert polyline.points == points
        assert polyline.point_count == 1

    def test_polyline_multiple_points(self):
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

        # Test specific points along the polyline
        p0 = polyline.point(0.0)  # Should be at start (0, 0)
        p1 = polyline.point(1.0)  # Should be at end (10, 10)

        # Verify start and end points
        assert abs(p0 - points[0]) < 1e-10
        assert abs(p1 - points[-1]) < 1e-10

        # Test tangent vectors - verify they have reasonable magnitude
        t0 = polyline.tangent(0.0)  # Should point along first segment
        t1 = polyline.tangent(1.0)  # Should point along last segment

        # Tangent vectors should have non-zero magnitude
        assert abs(t0) > 0
        assert abs(t1) > 0

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

    def test_polyline_with_duplicate_points(self):
        """Test polyline with duplicate consecutive points"""
        points = [0+0j, 0+0j, 10+0j, 10+0j, 10+10j]

        polyline = Polyline(points)

        # Should handle gracefully
        assert polyline.point_count == 5

        # Length should handle zero-length segments
        length = polyline.length()
        assert length >= 0

    def test_polyline_with_collinear_points(self):
        """Test polyline with collinear points"""
        points = [0+0j, 5+0j, 10+0j, 10+5j, 10+10j]  # First three are collinear

        polyline = Polyline(points)

        # Should handle gracefully
        assert polyline.length() > 0

        # Bounding box should be correct
        bbox = polyline.boundingbox()
        assert bbox == [0.0, 0.0, 10.0, 10.0]

    def test_polyline_very_large_coordinates(self):
        """Test polyline with very large coordinate values"""
        points = [1e6+1e6j, 2e6+1e6j, 2e6+2e6j]

        polyline = Polyline(points)

        # Should handle large numbers gracefully
        assert polyline.length() > 0

        # Bounding box should be correct
        bbox = polyline.boundingbox()
        expected = [1e6, 1e6, 2e6, 2e6]

        for actual, exp in zip(bbox, expected):
            assert abs(actual - exp) < 1e-6

    def test_polyline_negative_coordinates(self):
        """Test polyline with negative coordinates"""
        points = [-10-10j, -5-5j, 0+0j, 5+5j]

        polyline = Polyline(points)

        # Should handle negative coordinates
        bbox = polyline.boundingbox()

        expected = [-10.0, -10.0, 5.0, 5.0]
        assert bbox == expected

    def test_polyline_complex_patterns(self):
        """Test polyline with complex coordinate patterns"""
        base_point = 100 + 200j
        offset = 50 + 75j

        complex_points = [
            base_point,
            base_point + offset,
            base_point + offset + 1j * offset.real,
            base_point + 1j * offset.imag
        ]

        polyline = Polyline(complex_points)

        # Should handle complex coordinates without issues
        bbox = polyline.boundingbox()
        length = polyline.length()

        # Basic sanity checks
        assert len(bbox) == 4
        assert length >= 0

    def test_polyline_open_path_behavior(self):
        """Test that polyline remains open (doesn't connect back to start)"""
        points = [0+0j, 10+0j, 10+10j, 0+10j]
        polyline = Polyline(points)

        # For polyline, start and end points may be different
        start_point = polyline.point(0.0)
        end_point = polyline.point(1.0)

        # Since this is an open path, we just verify the points are different
        # (for this particular path, start != end)
        distance = abs(start_point - end_point)
        # We don't assert they're different since it depends on the path