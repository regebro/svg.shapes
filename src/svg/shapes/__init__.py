"""SVG Shapes Library

This library extends svg.path by providing implementations of other SVG shapes
(Rectangle, Circle, Ellipse, Polyline, Polygon) that follow the same API patterns.

All shapes can be converted to svg.path.Path objects and provide the same core methods:
- point(pos): Get a point along the shape's perimeter
- tangent(pos): Get the tangent vector at a position
- length(): Calculate the total length
- boundingbox(): Get the bounding rectangle

For convenience, Line and Path are re-exported from svg.path.
"""

from __future__ import annotations

# Re-export core classes from svg.path for convenience
from svg.path import Path, Line

# Import base classes
from .base import Shape

# Import shape classes
from .shapes import Rectangle, Circle, Ellipse, Polyline, Polygon

__version__ = "0.1.dev0"

# Export all available classes
__all__ = [
    "Path",
    "Line",
    "Shape",
    "Rectangle",
    "Circle",
    "Ellipse",
    "Polyline",
    "Polygon",
]

