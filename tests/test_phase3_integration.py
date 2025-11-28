"""Integration tests for Phase 3 shapes"""

import pytest


def test_import_all_phase3_shapes():
    """Test that all Phase 3 shapes can be imported"""
    from svg.shapes import Rectangle, Circle, Ellipse, Shape

    # Test that classes are available
    assert Rectangle is not None
    assert Circle is not None
    assert Ellipse is not None
    assert Shape is not None


def test_create_all_phase3_shapes():
    """Test creating instances of all Phase 3 shapes"""
    from svg.shapes import Rectangle, Circle, Ellipse

    # Test creation without errors
    rect = Rectangle(start=0+0j, size=10+5j)
    circle = Circle(center=0+0j, r=5)
    ellipse = Ellipse(center=0+0j, r=5+3j)

    # Test that they're the right types
    assert isinstance(rect, Rectangle)
    assert isinstance(circle, Circle)
    assert isinstance(ellipse, Ellipse)


def test_basic_shape_operations():
    """Test basic operations work on all Phase 3 shapes"""
    from svg.shapes import Rectangle, Circle, Ellipse

    shapes = [
        Rectangle(start=0+0j, size=10+5j),
        Circle(center=0+0j, r=5),
        Ellipse(center=0+0j, r=5+3j)
    ]

    for shape in shapes:
        # Test basic operations
        point = shape.point(0.5)
        tangent = shape.tangent(0.5)
        length = shape.length()
        bbox = shape.boundingbox()

        # Basic type checks
        assert isinstance(point, complex)
        assert isinstance(tangent, complex)
        assert isinstance(length, (int, float))
        assert isinstance(bbox, list)
        assert len(bbox) == 4
        assert length > 0


def test_svg_path_integration():
    """Test integration with svg.path (if available)"""
    from svg.shapes import Rectangle, Circle, Ellipse

    shapes = [
        Rectangle(start=0+0j, size=10+5j),
        Circle(center=0+0j, r=5),
        Ellipse(center=0+0j, r=5+3j)
    ]

    for shape in shapes:
        try:
            path = shape.to_path()
            # If svg.path is available, should return a Path object
            assert path is not None
            # Test that the path has the expected methods
            assert hasattr(path, 'point')
            assert hasattr(path, 'length')
        except ImportError:
            # svg.path not available, which is OK for testing
            pass


def test_shape_equality_and_repr():
    """Test equality and string representation work properly"""
    from svg.shapes import Rectangle, Circle, Ellipse

    # Test Rectangle
    rect1 = Rectangle(start=1+2j, size=10+5j)
    rect2 = Rectangle(start=1+2j, size=10+5j)
    rect3 = Rectangle(start=1+2j, size=10+6j)

    assert rect1 == rect2
    assert rect1 != rect3
    assert "Rectangle" in str(rect1)

    # Test Circle
    circle1 = Circle(center=1+2j, r=5)
    circle2 = Circle(center=1+2j, r=5)
    circle3 = Circle(center=1+2j, r=6)

    assert circle1 == circle2
    assert circle1 != circle3
    assert "Circle" in str(circle1)

    # Test Ellipse
    ellipse1 = Ellipse(center=1+2j, r=5+3j)
    ellipse2 = Ellipse(center=1+2j, r=5+3j)
    ellipse3 = Ellipse(center=1+2j, r=6+3j)

    assert ellipse1 == ellipse2
    assert ellipse1 != ellipse3
    assert "Ellipse" in str(ellipse1)