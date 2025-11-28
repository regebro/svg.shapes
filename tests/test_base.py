"""Tests for base classes and utilities"""

import pytest
import math
from svg.shapes.base import (
    Shape,
    normalize_angle,
    point_to_complex,
    complex_to_point,
    distance
)


class TestShape:
    """Test the abstract Shape base class"""

    def test_shape_is_abstract(self):
        """Test that Shape cannot be instantiated directly"""
        with pytest.raises(TypeError):
            Shape()

    def test_shape_requires_all_methods(self):
        """Test that subclasses must implement all abstract methods"""

        class IncompleteShape(Shape):
            def __init__(self):
                super().__init__()

            # Missing: point, tangent, length, boundingbox, to_path, __eq__, __repr__

        with pytest.raises(TypeError):
            IncompleteShape()


class MockShape(Shape):
    """A minimal concrete Shape implementation for testing"""

    def __init__(self, test_length: float = 10.0):
        super().__init__()
        self._test_length = test_length

    def point(self, pos: float) -> complex:
        # Simple line from 0+0j to test_length+0j
        return complex(pos * self._test_length, 0)

    def tangent(self, pos: float) -> complex:
        # Constant tangent for straight line
        return complex(1, 0)

    def length(self, error: float = 1e-12, min_depth: int = 5) -> float:
        return self._test_length

    def boundingbox(self) -> list[float]:
        return [0.0, 0.0, self._test_length, 0.0]

    def to_path(self):
        # Import here to avoid circular imports during testing
        try:
            from svg.path import Path, Move, Line
            return Path(Move(0+0j), Line(0+0j, self._test_length+0j))
        except ImportError:
            # For testing without svg.path installed
            return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MockShape):
            return False
        return self._test_length == other._test_length

    def __repr__(self) -> str:
        return f"MockShape(length={self._test_length})"


class TestMockShape:
    """Test our mock shape implementation"""

    def test_mock_shape_creation(self):
        """Test creating a mock shape"""
        shape = MockShape(5.0)
        assert shape.length() == 5.0
        assert shape.point(0) == 0+0j
        assert shape.point(1) == 5+0j
        assert shape.point(0.5) == 2.5+0j

    def test_mock_shape_equality(self):
        """Test shape equality"""
        shape1 = MockShape(10.0)
        shape2 = MockShape(10.0)
        shape3 = MockShape(20.0)

        assert shape1 == shape2
        assert shape1 != shape3
        assert shape1 != "not a shape"

    def test_mock_shape_repr(self):
        """Test string representation"""
        shape = MockShape(15.0)
        assert repr(shape) == "MockShape(length=15.0)"

    def test_cache_clearing(self):
        """Test that cache is cleared properly"""
        shape = MockShape(10.0)

        # Access cached properties
        length1 = shape.length_via_path()

        # Clear cache
        shape._clear_cache()

        # Should be able to access again
        length2 = shape.length_via_path()
        assert length1 == length2


class TestUtilityFunctions:
    """Test utility functions in base module"""

    def test_normalize_angle(self):
        """Test angle normalization"""
        # Test basic cases
        assert normalize_angle(0) == 0
        assert abs(normalize_angle(2 * math.pi) - 0) < 1e-10
        assert abs(normalize_angle(math.pi) - math.pi) < 1e-10

        # Test negative angles
        assert abs(normalize_angle(-math.pi) - math.pi) < 1e-10
        assert abs(normalize_angle(-2 * math.pi) - 0) < 1e-10

        # Test angles > 2π
        assert abs(normalize_angle(3 * math.pi) - math.pi) < 1e-10
        assert abs(normalize_angle(4 * math.pi) - 0) < 1e-10

    def test_math_degrees_radians_available(self):
        """Test that math.radians and math.degrees are available"""
        # Test basic conversions using stdlib functions
        assert abs(math.radians(0) - 0) < 1e-10
        assert abs(math.radians(180) - math.pi) < 1e-10
        assert abs(math.radians(90) - math.pi/2) < 1e-10
        assert abs(math.radians(360) - 2*math.pi) < 1e-10

        # Test reverse conversions
        assert abs(math.degrees(0) - 0) < 1e-10
        assert abs(math.degrees(math.pi) - 180) < 1e-10
        assert abs(math.degrees(math.pi/2) - 90) < 1e-10
        assert abs(math.degrees(2*math.pi) - 360) < 1e-10

        # Test round-trip conversion
        for deg in [0, 30, 45, 90, 135, 180, 270, 360]:
            rad = math.radians(deg)
            deg2 = math.degrees(rad)
            assert abs(deg - deg2) < 1e-10

    def test_point_complex_conversion(self):
        """Test point to complex conversion"""
        # Test basic conversions
        assert point_to_complex(0, 0) == 0+0j
        assert point_to_complex(1, 2) == 1+2j
        assert point_to_complex(-1, -2) == -1-2j
        assert point_to_complex(3.5, -1.5) == 3.5-1.5j

        # Test reverse conversions
        assert complex_to_point(0+0j) == (0.0, 0.0)
        assert complex_to_point(1+2j) == (1.0, 2.0)
        assert complex_to_point(-1-2j) == (-1.0, -2.0)
        assert complex_to_point(3.5-1.5j) == (3.5, -1.5)

        # Test round-trip conversion
        points = [(0, 0), (1, 2), (-3, 4), (1.5, -2.5)]
        for x, y in points:
            c = point_to_complex(x, y)
            x2, y2 = complex_to_point(c)
            assert abs(x - x2) < 1e-10
            assert abs(y - y2) < 1e-10

    def test_distance(self):
        """Test distance calculation"""
        # Test basic distances
        assert distance(0+0j, 0+0j) == 0
        assert distance(0+0j, 1+0j) == 1
        assert distance(0+0j, 0+1j) == 1
        assert distance(0+0j, 3+4j) == 5  # 3-4-5 triangle

        # Test symmetric property
        p1, p2 = 1+2j, 4+6j
        assert distance(p1, p2) == distance(p2, p1)

        # Test with negative coordinates
        assert distance(-1-1j, 2+3j) == distance(0+0j, 3+4j)  # Same relative distance