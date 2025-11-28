svg.shapes
==========

svg.shapes is a collection of objects that implement SVG shape elements
(Rectangle, Circle, Ellipse, Polyline, Polygon) with the same API as svg.path.

This library extends the excellent svg.path library by providing implementations
for other SVG basic shapes that can be converted to path objects and provide
the same methods for geometric calculations.

Installation
------------

.. code-block:: bash

    pip install svg.shapes

Note: This will automatically install svg.path as a dependency.

Usage
-----

svg.shapes provides implementations for the basic SVG shapes with the same
API as svg.path segments. All coordinates are represented as complex numbers
where the real part is the X coordinate and the imaginary part is the Y coordinate.

.. code-block:: python

    from svg.shapes import Rectangle, Circle, Ellipse, Polyline, Polygon
    from svg.shapes import Path, Line  # Re-exported from svg.path

    # Create shapes using complex numbers for coordinates
    rect = Rectangle(start=10+20j, size=100+50j)  # top-left + width+height*j
    circle = Circle(center=50+50j, r=25)
    ellipse = Ellipse(center=100+100j, r=50+30j)  # rx + ry*j

    # Rounded rectangle
    rounded_rect = Rectangle(start=0+0j, size=100+50j, r=10+5j)  # rx + ry*j

    # All shapes support the same methods as svg.path segments
    length = rect.length()
    point_at_half = rect.point(0.5)
    tangent_at_quarter = rect.tangent(0.25)
    bbox = rect.boundingbox()

    # Convert shapes to paths for complex operations
    rect_path = rect.to_path()

    # Work with polylines and polygons
    points = [10+10j, 50+30j, 90+10j, 70+80j]
    polyline = Polyline(points)
    polygon = Polygon(points)  # Automatically closed

Features
--------

* **Complex Number Coordinates**: All positions use complex numbers (x + yj)
* **Unified Parameter System**: Dimensions and radii use complex numbers for consistency
* **Consistent API**: All shapes implement the same methods as svg.path segments
* **Path Conversion**: Any shape can be converted to an svg.path.Path object
* **Mathematical Accuracy**: Precise geometric calculations for all operations
* **SVG Compliance**: Shapes follow SVG specification exactly
* **Type Safety**: Full type hints and mypy compatibility
* **Performance**: Efficient implementations with caching where appropriate

Supported Shapes
----------------

* **Rectangle**: Regular and rounded rectangles
  - `Rectangle(start, size, r=0+0j)` where start is top-left, size is width+height*j, r is corner radius rx+ry*j
* **Circle**: Perfect circles using arc approximation
  - `Circle(center, r)` where center and radius are complex numbers
* **Ellipse**: Ellipses with different X and Y radii
  - `Ellipse(center, r)` where r is rx+ry*j for the two radii
* **Polyline**: Multi-point lines (not closed) - Coming in Phase 4
* **Polygon**: Multi-point closed shapes - Coming in Phase 4
* **Line**: Re-exported from svg.path
* **Path**: Re-exported from svg.path

Complex Number Coordinate System
--------------------------------

All coordinates in svg.shapes use complex numbers where:
- Real part = X coordinate
- Imaginary part = Y coordinate

Examples::

    position = 10 + 20j  # Point at (10, 20)
    size = 100 + 50j     # Width=100, Height=50
    radius = 5 + 3j      # rx=5, ry=3

Development Status
------------------

This library is currently in early development. The API may change before the 1.0 release.

License
-------

This module is under the MIT License, same as svg.path.

Dependencies
------------

* svg.path >= 6.0
* Python >= 3.8