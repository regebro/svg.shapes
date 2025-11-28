"""Shared test fixtures and configuration for svg.shapes tests"""

import pytest
import math


@pytest.fixture
def mock_svg_path():
    """Mock svg.path modules for testing without dependency"""

    class MockPath:
        def __init__(self, *segments):
            self.segments = segments

        def point(self, pos):
            # Simple implementation for testing
            return complex(pos * 10, 0)

        def tangent(self, pos):
            return complex(1, 0)

        def length(self, error=1e-12, min_depth=5):
            return 10.0

        def boundingbox(self):
            return [0.0, 0.0, 10.0, 0.0]

    class MockMove:
        def __init__(self, to):
            self.to = to

    class MockLine:
        def __init__(self, start, end):
            self.start = start
            self.end = end

    return {
        'Path': MockPath,
        'Move': MockMove,
        'Line': MockLine
    }


@pytest.fixture
def sample_points():
    """Sample point coordinates for testing"""
    return [
        0+0j,
        10+0j,
        10+10j,
        0+10j,
        5+5j,
        -5-5j,
        3.5+2.1j
    ]


@pytest.fixture
def sample_rectangles():
    """Sample rectangle parameters for testing"""
    return [
        {'x': 0, 'y': 0, 'width': 10, 'height': 5},
        {'x': 5, 'y': 10, 'width': 20, 'height': 15},
        {'x': -5, 'y': -10, 'width': 15, 'height': 8},
        {'x': 0, 'y': 0, 'width': 1, 'height': 1}  # Unit square
    ]


@pytest.fixture
def sample_circles():
    """Sample circle parameters for testing"""
    return [
        {'cx': 0, 'cy': 0, 'r': 5},
        {'cx': 10, 'cy': 20, 'r': 15},
        {'cx': -5, 'cy': -10, 'r': 8},
        {'cx': 0, 'cy': 0, 'r': 1}  # Unit circle
    ]


@pytest.fixture
def sample_ellipses():
    """Sample ellipse parameters for testing"""
    return [
        {'cx': 0, 'cy': 0, 'rx': 5, 'ry': 3},
        {'cx': 10, 'cy': 20, 'rx': 15, 'ry': 8},
        {'cx': -5, 'cy': -10, 'rx': 12, 'ry': 6},
        {'cx': 0, 'cy': 0, 'rx': 1, 'ry': 1}  # Unit circle as ellipse
    ]


@pytest.fixture
def sample_polylines():
    """Sample polyline point lists for testing"""
    return [
        [0+0j, 10+0j],  # Simple line
        [0+0j, 5+5j, 10+0j],  # Triangle path
        [0+0j, 10+0j, 10+10j, 0+10j],  # Rectangle path
        [i+1j*math.sin(i*math.pi/4) for i in range(8)]  # Sine wave
    ]


@pytest.fixture
def precision_tolerance():
    """Default precision tolerance for floating point comparisons"""
    return 1e-10