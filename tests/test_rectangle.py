"""Tests for Rectangle shape"""

import pytest
from svg.shapes.shapes import Rectangle


class TestRectangle:
    """Test the Rectangle shape implementation"""

    def test_rectangle_creation(self):
        """Test creating rectangles with valid parameters"""
        rect = Rectangle(start=0+0j, size=10+5j)
        assert rect.start == 0+0j
        assert rect.size == 10+5j
        assert rect.width == 10
        assert rect.height == 5
        assert rect.rx == 0
        assert rect.ry == 0
        assert not rect.is_rounded

    def test_rectangle_with_corner_radii(self):
        """Test creating rectangles with corner radii"""
        rect = Rectangle(start=0+0j, size=10+5j, r=2+3j)
        assert rect.r == 2+3j
        assert rect.is_rounded

    def test_rectangle_single_radius(self):
        """Test SVG behavior: single radius applies to both axes"""
        rect1 = Rectangle(start=0+0j, size=10+5j, r=2+0j)
        assert rect1.rx == 2
        assert rect1.ry == 2

    def test_rectangle_radius_limiting(self):
        """Test that corner radii are limited to half rectangle dimensions"""
        # rx larger than width/2
        rect1 = Rectangle(start=0+0j, size=10+20j, r=6+2j)
        assert rect1.rx == 5  # Limited to width/2
        assert rect1.ry == 2

        # ry larger than height/2
        rect2 = Rectangle(start=0+0j, size=20+10j, r=2+6j)
        assert rect2.rx == 2
        assert rect2.ry == 5  # Limited to height/2

    def test_rectangle_equality(self):
        """Test rectangle equality comparison"""
        rect1 = Rectangle(start=1+2j, size=10+5j)
        rect2 = Rectangle(start=1+2j, size=10+5j)
        rect3 = Rectangle(start=1+2j, size=10+6j)
        rect4 = Rectangle(start=1+2j, size=10+5j, r=1+0j)

        assert rect1 == rect2
        assert rect1 != rect3
        assert rect1 != rect4
        assert rect1 != "not a rectangle"

    def test_rectangle_repr(self):
        """Test string representation"""
        rect1 = Rectangle(start=1+2j, size=10+5j)
        assert repr(rect1) == "Rectangle(start=(1+2j), size=(10+5j))"

        rect2 = Rectangle(start=1+2j, size=10+5j, r=2+3j)
        assert repr(rect2) == "Rectangle(start=(1+2j), size=(10+5j), r=(2+3j))"

    def test_rectangle_boundingbox(self):
        """Test bounding box calculation"""
        rect = Rectangle(start=5+10j, size=20+15j)
        bbox = rect.boundingbox()
        assert bbox == [5, 10, 25, 25]

    def test_rectangle_length_simple(self):
        """Test perimeter calculation for simple rectangles"""
        rect = Rectangle(start=0+0j, size=10+5j)
        assert rect.length() == 30  # 2 * (10 + 5)

    def test_rectangle_point_simple(self):
        """Test point calculation for simple rectangles"""
        rect = Rectangle(start=0+0j, size=10+5j)

        # Test corner points (approximate positions)
        # Note: exact positions depend on path traversal order
        p0 = rect.point(0.0)  # Start point
        p1 = rect.point(1.0)  # End point (should be same as start for closed shapes)

        # For closed shapes, start and end points should be the same
        assert abs(p0 - p1) < 1e-6

    def test_rectangle_closed_shape(self):
        """Test that rectangle is properly closed"""
        rect = Rectangle(start=0+0j, size=10+5j)

        start_point = rect.point(0.0)
        end_point = rect.point(1.0)
        distance = abs(end_point - start_point)
        assert distance < 1e-6, "Rectangle not properly closed"

    def test_rectangle_complex_coordinates(self):
        """Test rectangle with complex coordinate patterns"""
        base_point = 100 + 200j
        size = 50 + 75j

        rect = Rectangle(start=base_point, size=size)

        bbox = rect.boundingbox()
        length = rect.length()

        # Basic sanity checks
        assert len(bbox) == 4
        assert length >= 0

    def test_rectangle_rounded_corners(self):
        """Test rectangle with rounded corners"""
        rect = Rectangle(start=0+0j, size=20+10j, r=3+2j)

        assert rect.is_rounded
        assert rect.rx == 3
        assert rect.ry == 2

        # Should still have valid bounding box and length
        bbox = rect.boundingbox()
        length = rect.length()

        assert bbox == [0, 0, 20, 10]
        assert length > 0

    def test_rectangle_to_path(self):
        """Test path conversion"""
        rect = Rectangle(start=0+0j, size=10+5j)
        path = rect.to_path()

        assert path is not None
        assert len(path) == 5  # Move + 4 Lines + Close

    def test_rectangle_to_path_rounded(self):
        """Test path conversion for rounded rectangle"""
        rect = Rectangle(start=0+0j, size=10+5j, r=2+1j)
        path = rect.to_path()

        assert path is not None
        assert len(path) > 5  # More segments due to arcs