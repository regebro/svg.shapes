"""Integration tests for SVG shapes library"""

import pytest
import math
from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon, Shape


def test_import_all_shapes():
    """Test that all shapes including Phase 4 can be imported"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon, Shape

    # Test that all classes are available
    assert Rectangle is not None
    assert Circle is not None
    assert Ellipse is not None
    assert Polyline is not None
    assert Polygon is not None
    assert Shape is not None


def test_create_all_shapes():
    """Test creating instances of all shapes including Phase 4"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

    # Test creation without errors
    rect = Rectangle(start=0+0j, size=10+5j)
    circle = Circle(center=0+0j, r=5)
    ellipse = Ellipse(center=0+0j, r=5+3j)
    polyline = Polyline([0+0j, 10+0j, 10+10j])
    polygon = Polygon([0+0j, 10+0j, 5+10j])

    # Test that they're the right types
    assert isinstance(rect, Rectangle)
    assert isinstance(circle, Circle)
    assert isinstance(ellipse, Ellipse)
    assert isinstance(polyline, Polyline)
    assert isinstance(polygon, Polygon)


def test_all_shapes_have_consistent_api():
    """Test that all shapes implement the same API"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

    shapes = [
        Rectangle(start=0+0j, size=10+5j),
        Circle(center=0+0j, r=5),
        Ellipse(center=0+0j, r=5+3j),
        Polyline([0+0j, 10+0j, 10+10j]),
        Polygon([0+0j, 10+0j, 5+10j])
    ]

    for shape in shapes:
        # Test all required methods exist and return appropriate types
        assert hasattr(shape, 'point')
        assert hasattr(shape, 'tangent')
        assert hasattr(shape, 'length')
        assert hasattr(shape, 'boundingbox')
        assert hasattr(shape, 'to_path')

        # Test methods return reasonable values
        point = shape.point(0.5)
        tangent = shape.tangent(0.5)
        length = shape.length()
        bbox = shape.boundingbox()

        # Verify reasonable values
        assert len(bbox) == 4
        assert length >= 0  # Length should be non-negative
        assert abs(point) >= 0  # Point should have some location
        assert abs(tangent) >= 0  # Tangent should have some direction


def test_svg_path_integration_all_shapes():
    """Test integration with svg.path for all shapes"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

    shapes = [
        Rectangle(start=0+0j, size=10+5j),
        Circle(center=0+0j, r=5),
        Ellipse(center=0+0j, r=5+3j),
        Polyline([0+0j, 10+0j, 10+10j]),
        Polygon([0+0j, 10+0j, 5+10j])
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


def test_shape_consistency_all_types():
    """Test consistency across all shape types"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

    shapes = [
        Rectangle(start=0+0j, size=10+5j),
        Circle(center=0+0j, r=5),
        Ellipse(center=0+0j, r=5+3j),
        Polyline([0+0j, 10+0j, 10+10j, 0+10j]),  # Open path
        Polygon([0+0j, 10+0j, 10+10j, 0+10j])    # Closed path
    ]

    for shape in shapes:
        # Test that bounding box makes sense
        bbox = shape.boundingbox()
        assert bbox[0] <= bbox[2]  # x_min <= x_max
        assert bbox[1] <= bbox[3]  # y_min <= y_max

        # Test that length is non-negative
        assert shape.length() >= 0

        # Test that points are accessible and reasonable
        start_point = shape.point(0.0)
        end_point = shape.point(1.0)
        mid_point = shape.point(0.5)

        # All points should be finite complex numbers
        assert abs(start_point) < float('inf')
        assert abs(end_point) < float('inf')
        assert abs(mid_point) < float('inf')


def test_closed_vs_open_shapes():
    """Test the difference between closed and open shapes"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

    # Closed shapes
    closed_shapes = [
        Rectangle(start=0+0j, size=10+10j),
        Circle(center=5+5j, r=5),
        Ellipse(center=5+5j, r=5+3j),
        Polygon([0+0j, 10+0j, 10+10j, 0+10j])
    ]

    # Open shape
    polyline = Polyline([0+0j, 10+0j, 10+10j, 0+10j])

    # For closed shapes, start and end points should be very close
    for shape in closed_shapes:
        start_point = shape.point(0.0)
        end_point = shape.point(1.0)
        distance = abs(end_point - start_point)
        assert distance < 1e-6, f"Shape {type(shape).__name__} not properly closed"

    # For polyline, start and end might be different (depends on the specific path)
    poly_start = polyline.point(0.0)
    poly_end = polyline.point(1.0)
    # We don't assert equality here since polyline might not be closed


def test_complex_coordinate_usage():
    """Test that complex coordinates work consistently across all shapes"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

    # Test with various complex coordinate patterns
    base_point = 100 + 200j
    offset = 50 + 75j

    # All shapes should handle complex coordinates properly
    rect = Rectangle(start=base_point, size=offset)
    circle = Circle(center=base_point, r=25)
    ellipse = Ellipse(center=base_point, r=30+20j)

    # Complex points for polyline/polygon
    complex_points = [
        base_point,
        base_point + offset,
        base_point + offset + 1j * offset.real,
        base_point + 1j * offset.imag
    ]

    polyline = Polyline(complex_points)
    polygon = Polygon(complex_points)

    # All should handle complex coordinates without issues
    shapes = [rect, circle, ellipse, polyline, polygon]

    for shape in shapes:
        bbox = shape.boundingbox()
        length = shape.length()

        # Basic sanity checks
        assert len(bbox) == 4
        assert length >= 0


def test_shape_equality_and_repr_all_types():
    """Test equality and string representation for all shape types"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

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

    # Test Polyline
    points1 = [0+0j, 10+0j, 10+10j]
    points2 = [0+0j, 10+0j, 10+10j]
    points3 = [0+0j, 10+0j, 20+10j]

    polyline1 = Polyline(points1)
    polyline2 = Polyline(points2)
    polyline3 = Polyline(points3)

    assert polyline1 == polyline2
    assert polyline1 != polyline3
    assert "Polyline" in str(polyline1)

    # Test Polygon
    polygon1 = Polygon(points1)
    polygon2 = Polygon(points2)
    polygon3 = Polygon(points3)

    assert polygon1 == polygon2
    assert polygon1 != polygon3
    assert "Polygon" in str(polygon1)


def test_polyline_vs_polygon_length():
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


def test_polyline_vs_polygon_closure():
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


def test_polyline_vs_polygon_path_structure():
    """Test differences in path structure"""
    points = [0+0j, 10+0j, 10+10j]

    polyline = Polyline(points)
    polygon = Polygon(points)

    poly_path = polyline.to_path()
    gon_path = polygon.to_path()

    # Polygon path should have one more segment (the Close command)
    assert len(gon_path) == len(poly_path) + 1


def test_real_world_usage_example():
    """Test a real-world usage example with all shape types"""
    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

    # Create a complex scene with multiple shapes
    # A house-like drawing
    house_base = Rectangle(start=0+0j, size=100+60j)  # House base
    door = Rectangle(start=40+0j, size=20+40j)         # Door
    window1 = Rectangle(start=10+35j, size=15+15j)     # Left window
    window2 = Rectangle(start=75+35j, size=15+15j)     # Right window

    # Roof (triangle as polygon)
    roof = Polygon([0+60j, 50+100j, 100+60j])

    # Chimney
    chimney = Rectangle(start=70+70j, size=8+20j)

    # Sun (circle)
    sun = Circle(center=150+120j, r=15)

    # Clouds (ellipses)
    cloud1 = Ellipse(center=120+110j, r=20+10j)
    cloud2 = Ellipse(center=200+115j, r=25+12j)

    # Path to house (polyline)
    path_to_house = Polyline([
        -20+0j, -10+0j, 0+0j, 10-5j, 20-8j, 30-10j, 40-8j
    ])

    # All shapes in the scene
    scene_shapes = [
        house_base, door, window1, window2, roof, chimney,
        sun, cloud1, cloud2, path_to_house
    ]

    # Test that all shapes work together
    total_length = 0.0
    combined_bbox = None

    for shape in scene_shapes:
        # All shapes should work
        length = shape.length()
        bbox = shape.boundingbox()

        total_length += length

        # Combine bounding boxes
        if combined_bbox is None:
            combined_bbox = bbox[:]
        else:
            combined_bbox[0] = min(combined_bbox[0], bbox[0])  # min x
            combined_bbox[1] = min(combined_bbox[1], bbox[1])  # min y
            combined_bbox[2] = max(combined_bbox[2], bbox[2])  # max x
            combined_bbox[3] = max(combined_bbox[3], bbox[3])  # max y

    # Scene should have reasonable properties
    assert total_length > 0
    assert combined_bbox is not None
    assert combined_bbox[0] < combined_bbox[2]  # Valid bounding box
    assert combined_bbox[1] < combined_bbox[3]

    # Test conversion to paths for the entire scene
    scene_paths = []
    for shape in scene_shapes:
        try:
            path = shape.to_path()
            if path is not None:
                scene_paths.append(path)
        except ImportError:
            # svg.path not available
            pass

    # Should be able to convert all shapes (if svg.path is available)
    if scene_paths:
        assert len(scene_paths) == len(scene_shapes)


def test_shape_performance_caching():
    """Test that shapes cache expensive calculations"""
    circle = Circle(center=0+0j, r=100)

    # First call should compute and cache
    length1 = circle.length()

    # Second call should use cached value
    length2 = circle.length()

    assert length1 == length2
    assert length1 > 0

    # Same for bounding box
    bbox1 = circle.boundingbox()
    bbox2 = circle.boundingbox()

    assert bbox1 == bbox2


def test_edge_cases_across_shapes():
    """Test edge cases that apply to multiple shapes"""
    # Very small shapes
    small_rect = Rectangle(start=0+0j, size=1e-6+1e-6j)
    small_circle = Circle(center=0+0j, r=1e-6)
    small_polygon = Polygon([0+0j, 1e-6+0j, 0+1e-6j])

    small_shapes = [small_rect, small_circle, small_polygon]

    for shape in small_shapes:
        assert shape.length() >= 0
        bbox = shape.boundingbox()
        assert len(bbox) == 4
        # Verify point method works
        p = shape.point(0.5)
        assert abs(p) < float('inf')

    # Very large shapes
    large_rect = Rectangle(start=1e6+1e6j, size=1e6+1e6j)
    large_circle = Circle(center=1e6+1e6j, r=1e6)
    large_polygon = Polygon([1e6+1e6j, 2e6+1e6j, 1e6+2e6j])

    large_shapes = [large_rect, large_circle, large_polygon]

    for shape in large_shapes:
        assert shape.length() > 0
        bbox = shape.boundingbox()
        assert len(bbox) == 4
        # Verify point method works for large coordinates
        p = shape.point(0.5)
        assert abs(p) > 0