"""Tests for Circle shape"""

import pytest
import math
from svg.shapes.shapes import Circle


class TestCircle:
    """Test the Circle shape implementation"""

    def test_circle_equality(self):
        """Test circle equality comparison"""
        circle1 = Circle(center=5+10j, r=3)
        circle2 = Circle(center=5+10j, r=3)
        circle3 = Circle(center=5+10j, r=4)
        circle4 = Circle(center=6+10j, r=3)

        assert circle1 == circle2
        assert circle1 != circle3
        assert circle1 != circle4
        assert circle1 != "not a circle"

    def test_circle_repr(self):
        """Test string representation"""
        circle = Circle(center=5+10j, r=3)
        assert repr(circle) == "Circle(center=(5+10j), r=3)"

    def test_circle_boundingbox(self):
        """Test bounding box calculation"""
        circle = Circle(center=5+10j, r=3)
        bbox = circle.boundingbox()
        assert bbox == [2, 7, 8, 13]

    def test_circle_length(self):
        """Test circumference calculation"""
        circle = Circle(center=0+0j, r=5)
        expected = 2 * math.pi * 5
        assert abs(circle.length() - expected) < 1e-10

    def test_circle_point(self):
        """Test point calculation along circle perimeter"""
        circle = Circle(center=0+0j, r=5)

        # Test specific points
        p0 = circle.point(0.0)  # Right point (5, 0)
        assert abs(p0 - (5+0j)) < 1e-10

        p_quarter = circle.point(0.25)  # Top point (0, 5)
        assert abs(p_quarter - (0+5j)) < 1e-10

        p_half = circle.point(0.5)  # Left point (-5, 0)
        assert abs(p_half - (-5+0j)) < 1e-10

        p_three_quarter = circle.point(0.75)  # Bottom point (0, -5)
        assert abs(p_three_quarter - (0-5j)) < 1e-10

    def test_circle_tangent(self):
        """Test tangent calculation along circle perimeter"""
        circle = Circle(center=0+0j, r=5)

        # Test tangent vectors (should be perpendicular to radius)
        t0 = circle.tangent(0.0)  # At right point, tangent points up
        assert abs(t0 - (0+5j)) < 1e-10

        t_quarter = circle.tangent(0.25)  # At top point, tangent points left
        assert abs(t_quarter - (-5+0j)) < 1e-10

    def test_circle_centered_origin(self):
        """Test circle centered at origin"""
        circle = Circle(center=0+0j, r=1)

        # Unit circle should have circumference 2π
        assert abs(circle.length() - 2 * math.pi) < 1e-10

        # Bounding box should be [-1, -1, 1, 1]
        assert circle.boundingbox() == [-1, -1, 1, 1]

    def test_circle_closed_shape(self):
        """Test that circle is properly closed"""
        circle = Circle(center=0+0j, r=5)

        start_point = circle.point(0.0)
        end_point = circle.point(1.0)
        distance = abs(end_point - start_point)
        assert distance < 1e-6, "Circle not properly closed"

    def test_circle_complex_coordinates(self):
        """Test circle with complex coordinate patterns"""
        base_point = 150 + 120j
        radius = 25

        circle = Circle(center=base_point, r=radius)

        bbox = circle.boundingbox()
        length = circle.length()

        # Basic sanity checks
        assert len(bbox) == 4
        assert length >= 0

    def test_circle_to_path(self):
        """Test path conversion"""
        circle = Circle(center=0+0j, r=5)
        path = circle.to_path()

        assert path is not None
        assert len(path) == 6  # Move + 4 Arcs + Close

    def test_circle_point_and_tangent_consistency(self):
        """Test that point and tangent methods are consistent"""
        circle = Circle(center=0+0j, r=5)

        # Test at various positions
        for pos in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9]:
            point = circle.point(pos)
            tangent = circle.tangent(pos)

            # Point should be at distance r from center
            distance_from_center = abs(point - circle.center)
            assert abs(distance_from_center - circle.r) < 1e-10

            # Tangent should be perpendicular to radius vector
            radius_vector = point - circle.center
            dot_product = (tangent.conjugate() * radius_vector).real
            assert abs(dot_product) < 1e-10

    def test_circle_negative_coordinates(self):
        """Test circle with negative coordinates"""
        circle = Circle(center=-10-5j, r=3)

        bbox = circle.boundingbox()
        expected = [-13.0, -8.0, -7.0, -2.0]
        assert bbox == expected

        # Should still work normally
        assert circle.length() == 2 * math.pi * 3
        # Verify point calculation works
        p = circle.point(0.5)
        assert abs(p - (-13-5j)) < 1e-10  # Left point of circle