"""Base classes and utilities for SVG shapes

This module provides the abstract base class that all SVG shapes inherit from,
ensuring consistent API with svg.path segments.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Union, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from svg.path import Path

# Constants matching svg.path
MIN_DEPTH = 5
ERROR = 1e-12


class Shape(ABC):
    """Abstract base class for all SVG shapes

    This class defines the interface that all shapes must implement,
    ensuring consistency with svg.path segment API.

    All shapes must provide:
    - point(pos): Get a point along the shape's perimeter
    - tangent(pos): Get the tangent vector at a position
    - length(): Calculate the total perimeter length
    - boundingbox(): Get the bounding rectangle
    - to_path(): Convert to an svg.path.Path object
    """

    def __init__(self) -> None:
        """Initialize the shape

        Subclasses should call super().__init__() and set up their parameters.
        """
        self._path_cache: Union[Path, None] = None
        self._length_cache: Union[float, None] = None

    @abstractmethod
    def point(self, pos: float) -> complex:
        """Get a point along the shape's perimeter

        Args:
            pos: Position along the shape from 0.0 (start) to 1.0 (end)

        Returns:
            Complex number representing the (x, y) coordinate

        The position parameter should be normalized so that:
        - 0.0 returns the starting point of the shape
        - 1.0 returns the ending point of the shape
        - 0.5 returns the midpoint along the perimeter
        """
        pass

    @abstractmethod
    def tangent(self, pos: float) -> complex:
        """Get the tangent vector at a position along the shape

        Args:
            pos: Position along the shape from 0.0 to 1.0

        Returns:
            Complex number representing the tangent direction vector

        The tangent vector indicates the direction of the curve at the given position.
        """
        pass

    @abstractmethod
    def length(self, error: float = ERROR, min_depth: int = MIN_DEPTH) -> float:
        """Calculate the total perimeter length of the shape

        Args:
            error: Maximum error tolerance for approximation algorithms
            min_depth: Minimum recursion depth for approximation algorithms

        Returns:
            Total length of the shape's perimeter

        For simple shapes like rectangles this is exact, for curves it may be
        an approximation using the same algorithms as svg.path.
        """
        pass

    @abstractmethod
    def boundingbox(self) -> List[float]:
        """Get the bounding rectangle of the shape

        Returns:
            List of [x_min, y_min, x_max, y_max] coordinates

        This should return the smallest rectangle that completely contains
        the shape.
        """
        pass

    @abstractmethod
    def to_path(self) -> Path:
        """Convert the shape to an svg.path.Path object

        Returns:
            Path object representing the same shape

        This allows shapes to be used anywhere that svg.path objects are expected.
        The conversion should be cached for performance.
        """
        pass

    def _clear_cache(self) -> None:
        """Clear internal caches when shape parameters change"""
        self._path_cache = None
        self._length_cache = None

    # Default implementations using path conversion

    def point_via_path(self, pos: float) -> complex:
        """Default point() implementation via path conversion

        Subclasses can use this if they don't want to implement point() directly.
        """
        path = self.to_path()
        return path.point(pos)

    def tangent_via_path(self, pos: float) -> complex:
        """Default tangent() implementation via path conversion

        Subclasses can use this if they don't want to implement tangent() directly.
        """
        path = self.to_path()
        return path.tangent(pos)

    def length_via_path(self, error: float = ERROR, min_depth: int = MIN_DEPTH) -> float:
        """Default length() implementation via path conversion

        Subclasses can use this if they don't want to implement length() directly.
        """
        if self._length_cache is None:
            path = self.to_path()
            self._length_cache = path.length(error=error, min_depth=min_depth)
        return self._length_cache

    def boundingbox_via_path(self) -> List[float]:
        """Default boundingbox() implementation via path conversion

        Subclasses can use this if they don't want to implement boundingbox() directly.
        """
        path = self.to_path()
        return path.boundingbox()

    # Standard object methods that subclasses should override

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Test equality with another shape"""
        pass

    def __ne__(self, other: object) -> bool:
        """Test inequality with another shape"""
        return not self.__eq__(other)

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the shape"""
        pass


def normalize_angle(angle: float) -> float:
    """Normalize angle to [0, 2π) range

    Args:
        angle: Angle in radians

    Returns:
        Equivalent angle in [0, 2π) range
    """
    return angle % (2 * math.pi)




def point_to_complex(x: float, y: float) -> complex:
    """Convert x,y coordinates to complex number

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        Complex number with x as real part, y as imaginary part
    """
    return complex(x, y)


def complex_to_point(c: complex) -> tuple[float, float]:
    """Convert complex number to x,y coordinates

    Args:
        c: Complex number

    Returns:
        Tuple of (x, y) coordinates
    """
    return (c.real, c.imag)


def distance(p1: complex, p2: complex) -> float:
    """Calculate distance between two points

    Args:
        p1: First point as complex number
        p2: Second point as complex number

    Returns:
        Euclidean distance between the points
    """
    diff = p2 - p1
    return math.sqrt(diff.real**2 + diff.imag**2)


