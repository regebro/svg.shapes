"""Tests for Ellipse shape"""

import pytest
import math
from svg.shapes.shapes import Ellipse


class TestEllipse:
    """Test the Ellipse shape implementation"""

    def test_ellipse_creation(self):
        """Test creating ellipses with valid parameters"""
        ellipse = Ellipse(center=5+10j, r=3+2j)
        assert ellipse.center == 5+10j
        assert ellipse.r == 3+2j
        assert not ellipse.is_circle

    def test_ellipse_as_circle(self):
        """Test ellipse with equal radii (circle)"""
        ellipse = Ellipse(center=0+0j, r=5+0j)
        assert ellipse.is_circle

        # Also test with explicit equal radii
        ellipse2 = Ellipse(center=0+0j, r=5+5j)
        assert ellipse2.is_circle

    def test_ellipse_equality(self):
        """Test ellipse equality comparison"""
        ellipse1 = Ellipse(center=5+10j, r=3+2j)
        ellipse2 = Ellipse(center=5+10j, r=3+2j)
        ellipse3 = Ellipse(center=5+10j, r=4+2j)
        ellipse4 = Ellipse(center=6+10j, r=3+2j)

        assert ellipse1 == ellipse2
        assert ellipse1 != ellipse3
        assert ellipse1 != ellipse4
        assert ellipse1 != "not an ellipse"

    def test_ellipse_repr(self):
        """Test string representation"""
        ellipse = Ellipse(center=5+10j, r=3+2j)
        assert repr(ellipse) == "Ellipse(center=(5+10j), r=(3+2j))"

    def test_ellipse_boundingbox(self):
        """Test bounding box calculation"""
        ellipse = Ellipse(center=5+10j, r=3+2j)
        bbox = ellipse.boundingbox()
        assert bbox == [2, 8, 8, 12]

    def test_ellipse_point(self):
        """Test point calculation along ellipse perimeter"""
        ellipse = Ellipse(center=0+0j, r=5+3j)

        # Test specific points
        p0 = ellipse.point(0.0)  # Right point (5, 0)
        assert abs(p0 - (5+0j)) < 1e-10

        p_quarter = ellipse.point(0.25)  # Top point (0, 3)
        assert abs(p_quarter - (0+3j)) < 1e-10

        p_half = ellipse.point(0.5)  # Left point (-5, 0)
        assert abs(p_half - (-5+0j)) < 1e-10

        p_three_quarter = ellipse.point(0.75)  # Bottom point (0, -3)
        assert abs(p_three_quarter - (0-3j)) < 1e-10

    def test_ellipse_tangent(self):
        """Test tangent calculation along ellipse perimeter"""
        ellipse = Ellipse(center=0+0j, r=5+3j)

        # Test tangent vectors at cardinal points
        t0 = ellipse.tangent(0.0)  # At right point
        assert abs(t0.real - 0) < 1e-10  # dx should be 0
        assert t0.imag > 0  # dy should be positive (pointing up)

        t_quarter = ellipse.tangent(0.25)  # At top point
        assert t_quarter.real < 0  # dx should be negative (pointing left)
        assert abs(t_quarter.imag - 0) < 1e-10  # dy should be 0

    def test_ellipse_length_circle(self):
        """Test length calculation for circular ellipse"""
        ellipse = Ellipse(center=0+0j, r=5+0j)
        expected = 2 * math.pi * 5
        assert abs(ellipse.length() - expected) < 1e-10

    def test_ellipse_length_approximation(self):
        """Test length calculation uses reasonable approximation"""
        ellipse = Ellipse(center=0+0j, r=5+3j)
        length = ellipse.length()

        # Should be between the circumferences of inscribed and circumscribed circles
        min_length = 2 * math.pi * 3  # Smaller radius
        max_length = 2 * math.pi * 5  # Larger radius

        assert min_length < length < max_length

        # Ramanujan's approximation should be reasonably accurate
        # For this ellipse, we can verify it's in the right ballpark
        assert 25 < length < 30  # Reasonable range for this ellipse

    def test_ellipse_closed_shape(self):
        """Test that ellipse is properly closed"""
        ellipse = Ellipse(center=0+0j, r=5+3j)

        start_point = ellipse.point(0.0)
        end_point = ellipse.point(1.0)
        distance = abs(end_point - start_point)
        assert distance < 1e-6, "Ellipse not properly closed"

    def test_ellipse_complex_coordinates(self):
        """Test ellipse with complex coordinate patterns"""
        base_point = 120 + 110j
        radii = 30 + 20j

        ellipse = Ellipse(center=base_point, r=radii)

        bbox = ellipse.boundingbox()
        length = ellipse.length()

        # Basic sanity checks
        assert len(bbox) == 4
        assert length >= 0

    def test_ellipse_to_path(self):
        """Test path conversion"""
        ellipse = Ellipse(center=0+0j, r=5+3j)
        path = ellipse.to_path()

        assert path is not None
        assert len(path) == 6  # Move + 4 Arcs + Close

    def test_ellipse_degenerate_cases(self):
        """Test ellipse with unusual radius values"""
        # Single radius component (should behave like circle)
        ellipse1 = Ellipse(center=0+0j, r=5+0j)
        assert ellipse1.is_circle

        # Very small ellipse
        ellipse2 = Ellipse(center=0+0j, r=0.1+0.05j)
        assert ellipse2.length() > 0
        assert len(ellipse2.boundingbox()) == 4

    def test_ellipse_real_number_radius(self):
        """Test ellipse with real number as radius (should create circle)"""
        ellipse = Ellipse(center=5+5j, r=3+0j)
        assert ellipse.is_circle

        # Should behave like a circle
        expected_circumference = 2 * math.pi * 3
        assert abs(ellipse.length() - expected_circumference) < 1e-10

    def test_ellipse_negative_coordinates(self):
        """Test ellipse with negative coordinates"""
        ellipse = Ellipse(center=-10-5j, r=3+2j)

        bbox = ellipse.boundingbox()
        expected = [-13.0, -7.0, -7.0, -3.0]
        assert bbox == expected

        # Should still work normally
        assert ellipse.length() > 0
        # Verify point calculation works
        p = ellipse.point(0.5)
        assert abs(p - (-13-5j)) < 1e-10  # Left point of ellipse

    def test_ellipse_large_coordinates(self):
        """Test ellipse with very large coordinate values"""
        ellipse = Ellipse(center=1e6+1e6j, r=1e3+5e2j)

        # Should handle large numbers gracefully
        assert ellipse.length() > 0

        # Bounding box should be correct
        bbox = ellipse.boundingbox()
        expected = [1e6-1e3, 1e6-5e2, 1e6+1e3, 1e6+5e2]

        for actual, exp in zip(bbox, expected):
            assert abs(actual - exp) < 1e-6