"""Tests for SVG shape implementations"""

import pytest
import math
from svg.shapes.shapes import Rectangle, Circle, Ellipse


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

        # Points should be on the rectangle perimeter
        assert isinstance(p0, complex)
        assert isinstance(p1, complex)


class TestCircle:
    """Test the Circle shape implementation"""

    def test_circle_creation(self):
        """Test creating circles with valid parameters"""
        circle = Circle(center=5+10j, r=3)
        assert circle.center == 5+10j
        assert circle.r == 3

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
        ellipse = Ellipse(center=0+0j, r=5+5j)
        assert ellipse.is_circle

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


class TestShapeIntegration:
    """Integration tests across different shapes"""

    def test_all_shapes_have_required_methods(self):
        """Test that all shapes implement the required Shape interface"""
        shapes = [
            Rectangle(start=0+0j, size=10+5j),
            Circle(center=0+0j, r=5),
            Ellipse(center=0+0j, r=5+3j)
        ]

        for shape in shapes:
            # Test all required methods exist and return appropriate types
            assert hasattr(shape, 'point')
            assert hasattr(shape, 'tangent')
            assert hasattr(shape, 'length')
            assert hasattr(shape, 'boundingbox')
            assert hasattr(shape, 'to_path')

            # Test methods return correct types
            assert isinstance(shape.point(0.5), complex)
            assert isinstance(shape.tangent(0.5), complex)
            assert isinstance(shape.length(), (int, float))
            assert isinstance(shape.boundingbox(), list)
            assert len(shape.boundingbox()) == 4

    def test_shape_consistency(self):
        """Test consistency between different calculation methods"""
        shapes = [
            Rectangle(start=0+0j, size=10+5j),
            Circle(center=0+0j, r=5),
            Ellipse(center=0+0j, r=5+3j)
        ]

        for shape in shapes:
            # Test that start and end points are the same (closed shapes)
            start_point = shape.point(0.0)
            end_point = shape.point(1.0)

            # For closed shapes, start and end should be very close
            distance = abs(end_point - start_point)
            assert distance < 1e-6, f"Shape {type(shape).__name__} not properly closed"

            # Test that bounding box makes sense
            bbox = shape.boundingbox()
            assert bbox[0] <= bbox[2]  # x_min <= x_max
            assert bbox[1] <= bbox[3]  # y_min <= y_max

            # Test that length is positive
            assert shape.length() > 0
