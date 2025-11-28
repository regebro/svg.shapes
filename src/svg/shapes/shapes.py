"""SVG Shape implementations

This module contains implementations of the basic SVG shapes:
Rectangle, Circle, Ellipse, Polyline, and Polygon.

All shapes follow the same API as svg.path segments and can be converted
to Path objects for complex operations.
"""

from __future__ import annotations
from typing import List, Union
import math

from .base import (
    Shape,
    normalize_angle,
    point_to_complex,
    distance
)

from svg.path import Path, Move, Line, Arc, Close


class Rectangle(Shape):
    """SVG Rectangle shape

    Represents an SVG <rect> element with optional rounded corners.

    Args:
        start: Top-left corner position as complex number (x + yj)
        size: Rectangle dimensions as complex number (width + height*j)
        r: Corner radius as complex number (rx + ry*j), optional

    The rectangle can have rounded corners if r is specified.
    If r is a real number, both corner radii are set to that value.
    """

    def __init__(
        self,
        start: complex,
        size: complex,
        r: complex = 0+0j
    ) -> None:
        super().__init__()

        self.start = start
        self.size = size
        self.r = r

        # Convert to individual components for internal calculations
        self.width = self.size.real
        self.height = self.size.imag
        self.rx = self.r.real
        self.ry = self.r.imag

        # SVG spec: if only one radius component is specified, use it for both
        if self.rx > 0 and self.ry == 0:
            self.ry = self.rx
        elif self.ry > 0 and self.rx == 0:
            self.rx = self.ry

        # SVG spec: limit radii to half the rectangle dimensions
        if self.width > 0:
            self.rx = min(self.rx, abs(self.width) / 2)
        if self.height > 0:
            self.ry = min(self.ry, abs(self.height) / 2)

    def __repr__(self) -> str:
        if self.r != 0+0j:
            return f"Rectangle(start={self.start}, size={self.size}, r={self.r})"
        else:
            return f"Rectangle(start={self.start}, size={self.size})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return False
        return (
            self.start == other.start and
            self.size == other.size and
            self.r == other.r
        )

    @property
    def is_rounded(self) -> bool:
        """True if the rectangle has rounded corners"""
        return self.rx > 0 or self.ry > 0

    def to_path(self) -> Path:
        """Convert rectangle to svg.path.Path object"""

        if self._path_cache is not None:
            return self._path_cache

        if not self.is_rounded:
            # Simple rectangle with 4 straight lines
            top_left = self.start
            top_right = self.start + self.size.real
            bottom_right = self.start + self.size.real + 1j * self.size.imag
            bottom_left = self.start + 1j * self.size.imag

            self._path_cache = Path(
                Move(top_left),
                Line(top_left, top_right),
                Line(top_right, bottom_right),
                Line(bottom_right, bottom_left),
                Close(bottom_left, top_left)
            )
        else:
            # Rounded rectangle with arcs at corners
            self._path_cache = self._create_rounded_rectangle_path()

        return self._path_cache

    def _create_rounded_rectangle_path(self) -> Path:
        """Create path for rounded rectangle"""

        # Corner coordinates using complex numbers
        top_left = self.start
        bottom_right = self.start + self.size.real + 1j * self.size.imag

        # Actual corner radii (may be limited by rectangle size)
        rx, ry = self.rx, self.ry

        # Path segments
        segments = []

        # Start at top-left corner, after the rounded part
        start_point = top_left + rx
        segments.append(Move(start_point))

        # Top edge (if there's a straight part)
        if abs(self.size.real) > 2 * rx:
            segments.append(Line(start_point, bottom_right.real - rx + 1j * top_left.imag))

        # Top-right corner arc
        if rx > 0 and ry > 0:
            arc_start = bottom_right.real - rx + 1j * top_left.imag
            arc_end = bottom_right.real + 1j * (top_left.imag + ry)
            segments.append(Arc(
                start=arc_start,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,  # small arc
                sweep=True,  # clockwise
                end=arc_end
            ))

        # Right edge
        if abs(self.size.imag) > 2 * ry:
            segments.append(Line(
                bottom_right.real + 1j * (top_left.imag + ry),
                bottom_right.real + 1j * (bottom_right.imag - ry)
            ))

        # Bottom-right corner arc
        if rx > 0 and ry > 0:
            arc_start = bottom_right.real + 1j * (bottom_right.imag - ry)
            arc_end = bottom_right.real - rx + 1j * bottom_right.imag
            segments.append(Arc(
                start=arc_start,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,
                sweep=True,
                end=arc_end
            ))

        # Bottom edge
        if abs(self.size.real) > 2 * rx:
            segments.append(Line(
                bottom_right.real - rx + 1j * bottom_right.imag,
                top_left.real + rx + 1j * bottom_right.imag
            ))

        # Bottom-left corner arc
        if rx > 0 and ry > 0:
            arc_start = top_left.real + rx + 1j * bottom_right.imag
            arc_end = top_left.real + 1j * (bottom_right.imag - ry)
            segments.append(Arc(
                start=arc_start,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,
                sweep=True,
                end=arc_end
            ))

        # Left edge
        if abs(self.size.imag) > 2 * ry:
            segments.append(Line(
                top_left.real + 1j * (bottom_right.imag - ry),
                top_left.real + 1j * (top_left.imag + ry)
            ))

        # Top-left corner arc
        if rx > 0 and ry > 0:
            arc_start = top_left.real + 1j * (top_left.imag + ry)
            arc_end = top_left.real + rx + 1j * top_left.imag
            segments.append(Arc(
                start=arc_start,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,
                sweep=True,
                end=arc_end
            ))

        # Close the path
        segments.append(Close(segments[-1].end, start_point))

        return Path(*segments)

    def point(self, pos: float) -> complex:
        """Get point at position along rectangle perimeter"""
        return self.point_via_path(pos)

    def tangent(self, pos: float) -> complex:
        """Get tangent vector at position along rectangle perimeter"""
        return self.tangent_via_path(pos)

    def length(self, error: float = 1e-12, min_depth: int = 5) -> float:
        """Calculate perimeter length of rectangle"""
        if self._length_cache is None:
            if not self.is_rounded:
                # Simple perimeter calculation for rectangular shapes
                self._length_cache = 2 * (abs(self.size.real) + abs(self.size.imag))
            else:
                # For rounded rectangles, use path conversion
                self._length_cache = self.length_via_path(error, min_depth)
        return self._length_cache

    def boundingbox(self) -> List[float]:
        """Get bounding box of rectangle"""
        return [
            self.start.real,
            self.start.imag,
            self.start.real + self.size.real,
            self.start.imag + self.size.imag
        ]


class Circle(Shape):
    """SVG Circle shape

    Represents an SVG <circle> element.

    Args:
        center: Center position as complex number (x + yj)
        r: Radius

    The circle is approximated using 4 arc segments when converted to a path.
    """

    def __init__(self, center: complex, r: float) -> None:
        super().__init__()
        self.center = center
        self.r = r

    def __repr__(self) -> str:
        return f"Circle(center={self.center}, r={self.r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return False
        return (
            self.center == other.center and
            self.r == other.r
        )

    def to_path(self) -> Path:
        """Convert circle to svg.path.Path using 4 arc segments"""

        if self._path_cache is not None:
            return self._path_cache

        center = self.center
        radius = self.r

        # Four points around the circle: right, top, left, bottom
        right = center + radius
        top = center + 1j * radius
        left = center - radius
        bottom = center - 1j * radius

        # Create 4 arc segments that form a complete circle
        self._path_cache = Path(
            Move(right),
            Arc(
                start=right,
                radius=complex(radius, radius),
                rotation=0,
                arc=False,  # small arc
                sweep=True,  # clockwise
                end=bottom
            ),
            Arc(
                start=bottom,
                radius=complex(radius, radius),
                rotation=0,
                arc=False,
                sweep=True,
                end=left
            ),
            Arc(
                start=left,
                radius=complex(radius, radius),
                rotation=0,
                arc=False,
                sweep=True,
                end=top
            ),
            Arc(
                start=top,
                radius=complex(radius, radius),
                rotation=0,
                arc=False,
                sweep=True,
                end=right
            ),
            Close(top, right)
        )

        return self._path_cache

    def point(self, pos: float) -> complex:
        """Get point at position along circle perimeter"""
        # Direct calculation for better performance and accuracy
        angle = pos * 2 * math.pi
        return self.center + self.r * complex(math.cos(angle), math.sin(angle))

    def tangent(self, pos: float) -> complex:
        """Get tangent vector at position along circle perimeter"""
        # Tangent is perpendicular to radius
        angle = pos * 2 * math.pi
        return self.r * complex(-math.sin(angle), math.cos(angle))

    def length(self, error: float = 1e-12, min_depth: int = 5) -> float:
        """Calculate circumference of circle"""
        if self._length_cache is None:
            self._length_cache = 2 * math.pi * self.r
        return self._length_cache

    def boundingbox(self) -> List[float]:
        """Get bounding box of circle"""
        return [
            self.center.real - self.r,
            self.center.imag - self.r,
            self.center.real + self.r,
            self.center.imag + self.r
        ]


class Ellipse(Shape):
    """SVG Ellipse shape

    Represents an SVG <ellipse> element.

    Args:
        center: Center position as complex number (x + yj)
        r: Radius as complex number (rx + ry*j)

    The ellipse is approximated using 4 arc segments when converted to a path.
    If r is a real number, creates a circle with that radius.
    """

    def __init__(self, center: complex, r: complex) -> None:
        super().__init__()
        self.center = center
        self.r = r

    def __repr__(self) -> str:
        return f"Ellipse(center={self.center}, r={self.r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ellipse):
            return False
        return (
            self.center == other.center and
            self.r == other.r
        )

    @property
    def is_circle(self) -> bool:
        """True if this ellipse is actually a circle (rx == ry)"""
        return abs(abs(self.r.real) - abs(self.r.imag)) < 1e-10

    def to_path(self) -> Path:
        """Convert ellipse to svg.path.Path using 4 arc segments"""

        if self._path_cache is not None:
            return self._path_cache

        center = self.center

        # Get radius components from complex r
        rx = abs(self.r.real)
        ry = abs(self.r.imag) if self.r.imag != 0 else abs(self.r.real)

        # Four points around the ellipse: right, top, left, bottom
        right = center + rx
        top = center + 1j * ry
        left = center - rx
        bottom = center - 1j * ry

        # Create 4 arc segments that form a complete ellipse
        self._path_cache = Path(
            Move(right),
            Arc(
                start=right,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,  # small arc
                sweep=True,  # clockwise
                end=bottom
            ),
            Arc(
                start=bottom,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,
                sweep=True,
                end=left
            ),
            Arc(
                start=left,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,
                sweep=True,
                end=top
            ),
            Arc(
                start=top,
                radius=complex(rx, ry),
                rotation=0,
                arc=False,
                sweep=True,
                end=right
            ),
            Close(top, right)
        )

        return self._path_cache

    def point(self, pos: float) -> complex:
        """Get point at position along ellipse perimeter"""
        # Direct calculation using parametric form
        angle = pos * 2 * math.pi
        rx = abs(self.r.real)
        ry = abs(self.r.imag) if self.r.imag != 0 else abs(self.r.real)
        x = self.center.real + rx * math.cos(angle)
        y = self.center.imag + ry * math.sin(angle)
        return complex(x, y)

    def tangent(self, pos: float) -> complex:
        """Get tangent vector at position along ellipse perimeter"""
        # Derivative of parametric ellipse equation
        angle = pos * 2 * math.pi
        rx = abs(self.r.real)
        ry = abs(self.r.imag) if self.r.imag != 0 else abs(self.r.real)
        dx = -rx * math.sin(angle)
        dy = ry * math.cos(angle)
        return complex(dx, dy)

    def length(self, error: float = 1e-12, min_depth: int = 5) -> float:
        """Calculate perimeter of ellipse"""
        if self._length_cache is None:
            rx = abs(self.r.real)
            ry = abs(self.r.imag) if self.r.imag != 0 else abs(self.r.real)

            if self.is_circle:
                # Simple circumference for circles
                self._length_cache = 2 * math.pi * rx
            else:
                # Use Ramanujan's approximation for ellipse perimeter
                # This is quite accurate for most cases
                a, b = max(rx, ry), min(rx, ry)
                h = ((a - b) / (a + b)) ** 2
                self._length_cache = math.pi * (a + b) * (
                    1 + (3 * h) / (10 + math.sqrt(4 - 3 * h))
                )
        return self._length_cache

    def boundingbox(self) -> List[float]:
        """Get bounding box of ellipse"""
        rx = abs(self.r.real)
        ry = abs(self.r.imag) if self.r.imag != 0 else abs(self.r.real)
        return [
            self.center.real - rx,
            self.center.imag - ry,
            self.center.real + rx,
            self.center.imag + ry
        ]


class Polyline(Shape):
    """SVG Polyline shape

    Represents an SVG <polyline> element.

    Args:
        points: List of points as complex numbers

    A polyline is a series of connected straight line segments.
    Unlike a polygon, it is not automatically closed.
    """

    def __init__(self, points: List[complex]) -> None:
        super().__init__()
        self.points = list(points)  # Create a copy to avoid mutation issues

    def __repr__(self) -> str:
        return f"Polyline(points={self.points})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polyline):
            return False
        return self.points == other.points

    @property
    def point_count(self) -> int:
        """Number of points in the polyline"""
        return len(self.points)

    def to_path(self) -> Path:
        """Convert polyline to svg.path.Path object"""
        if self._path_cache is not None:
            return self._path_cache

        if len(self.points) == 0:
            # Empty polyline - create a degenerate path
            self._path_cache = Path()
        elif len(self.points) == 1:
            # Single point - create a Move command only
            self._path_cache = Path(Move(self.points[0]))
        else:
            # Multiple points - Move to first, Line to others
            segments = [Move(self.points[0])]
            for point in self.points[1:]:
                segments.append(Line(segments[-1].end, point))
            self._path_cache = Path(*segments)

        return self._path_cache

    def point(self, pos: float) -> complex:
        """Get point at position along polyline perimeter"""
        return self.point_via_path(pos)

    def tangent(self, pos: float) -> complex:
        """Get tangent vector at position along polyline perimeter"""
        return self.tangent_via_path(pos)

    def length(self, error: float = 1e-12, min_depth: int = 5) -> float:
        """Calculate total length of polyline"""
        if self._length_cache is None:
            if len(self.points) < 2:
                self._length_cache = 0.0
            else:
                # Calculate sum of distances between consecutive points
                total_length = 0.0
                for i in range(len(self.points) - 1):
                    segment_length = distance(self.points[i], self.points[i + 1])
                    total_length += segment_length
                self._length_cache = total_length
        return self._length_cache

    def boundingbox(self) -> List[float]:
        """Get bounding box of polyline"""
        if len(self.points) == 0:
            return [0.0, 0.0, 0.0, 0.0]

        x_coords = [p.real for p in self.points]
        y_coords = [p.imag for p in self.points]

        return [
            min(x_coords),
            min(y_coords),
            max(x_coords),
            max(y_coords)
        ]


class Polygon(Shape):
    """SVG Polygon shape

    Represents an SVG <polygon> element.

    Args:
        points: List of points as complex numbers

    A polygon is a closed shape made of straight line segments.
    The last point is automatically connected back to the first point.
    """

    def __init__(self, points: List[complex]) -> None:
        super().__init__()
        self.points = list(points)  # Create a copy to avoid mutation issues

    def __repr__(self) -> str:
        return f"Polygon(points={self.points})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polygon):
            return False
        return self.points == other.points

    @property
    def point_count(self) -> int:
        """Number of points in the polygon"""
        return len(self.points)

    def to_path(self) -> Path:
        """Convert polygon to svg.path.Path object"""
        if self._path_cache is not None:
            return self._path_cache

        if len(self.points) == 0:
            # Empty polygon - create a degenerate path
            self._path_cache = Path()
        elif len(self.points) == 1:
            # Single point - create a Move command only
            self._path_cache = Path(Move(self.points[0]))
        elif len(self.points) == 2:
            # Two points - create a line and close it (degenerate polygon)
            segments = [
                Move(self.points[0]),
                Line(self.points[0], self.points[1]),
                Close(self.points[1], self.points[0])
            ]
            self._path_cache = Path(*segments)
        else:
            # Multiple points - Move to first, Line to others, Close back to first
            segments = [Move(self.points[0])]
            for point in self.points[1:]:
                segments.append(Line(segments[-1].end, point))
            # Close the polygon
            segments.append(Close(segments[-1].end, self.points[0]))
            self._path_cache = Path(*segments)

        return self._path_cache

    def point(self, pos: float) -> complex:
        """Get point at position along polygon perimeter"""
        return self.point_via_path(pos)

    def tangent(self, pos: float) -> complex:
        """Get tangent vector at position along polygon perimeter"""
        return self.tangent_via_path(pos)

    def length(self, error: float = 1e-12, min_depth: int = 5) -> float:
        """Calculate total perimeter length of polygon"""
        if self._length_cache is None:
            if len(self.points) < 2:
                self._length_cache = 0.0
            elif len(self.points) == 2:
                # Two points - just the distance between them (times 2 for there and back)
                self._length_cache = 2 * distance(self.points[0], self.points[1])
            else:
                # Calculate sum of distances between consecutive points, plus closing edge
                total_length = 0.0
                for i in range(len(self.points) - 1):
                    segment_length = distance(self.points[i], self.points[i + 1])
                    total_length += segment_length
                # Add the closing edge from last point back to first
                total_length += distance(self.points[-1], self.points[0])
                self._length_cache = total_length
        return self._length_cache

    def boundingbox(self) -> List[float]:
        """Get bounding box of polygon"""
        if len(self.points) == 0:
            return [0.0, 0.0, 0.0, 0.0]

        x_coords = [p.real for p in self.points]
        y_coords = [p.imag for p in self.points]

        return [
            min(x_coords),
            min(y_coords),
            max(x_coords),
            max(y_coords)
        ]
