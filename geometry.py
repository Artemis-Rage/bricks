"""Geometry utilities for robotics."""

from umath import atan2, degrees, sqrt

def compute_trajectory(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
) -> tuple[float, float]:
    """Given a current and target positions, compute the heading and distance.

        Args:
        x0: initial x position.
        y0: initial y position.
        x1: target x position.
        y1: target y position.

    Returns: a pair of values (heading, distance) representing the heading and
      distance to drive to go from (x0, y0) to (x1, y1).
    """
    a = x1 - x0
    b = y1 - y0
    distance = sqrt(a**2 + b**2)
    heading = degrees(atan2(a, b))
    return heading, distance
