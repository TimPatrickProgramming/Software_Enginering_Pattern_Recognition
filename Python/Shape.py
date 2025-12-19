from abc import ABC, abstractmethod
import numpy as np
from typing import Union, Any

ApproxType = Union[np.ndarray, Any]

class Shape(ABC):
    """Abstract base class for geometric shapes detected in the image."""

    def __init__(self, approx: ApproxType, color_name: str) -> None:
        """
        Initializes the Shape object.

        Args:
            approx (ApproxType): The approximation array (NumPy array of vertices).
            color_name (str): The name of the detected color.
        """
        self.approx = approx
        self.color_name = color_name

class Triangle(Shape):
    """Represents a triangle shape."""
    def __init__(self, approx: ApproxType, color_name: str) -> None:
        """
        Args:
            approx (ApproxType): The approximation array of the contour vertices.
            color_name (str): The name of the color (e.g., 'red', 'blue').
        """
        super().__init__(approx, color_name)

class Rectangle(Shape):
    """Represents a rectangle shape (non-square)."""
    def __init__(self, approx: ApproxType, color_name: str) -> None:
        """
        Args:
            approx (ApproxType): The approximation array of the contour vertices.
            color_name (str): The name of the color (e.g., 'red', 'blue').
        """
        super().__init__(approx, color_name)

class Square(Shape):
    """Represents a square shape."""
    def __init__(self, approx: ApproxType, color_name: str) -> None:
        """
        Args:
            approx (ApproxType): The approximation array of the contour vertices.
            color_name (str): The name of the color (e.g., 'red', 'blue').
        """
        super().__init__(approx, color_name)

class Circle(Shape):
    """Represents a circle shape."""
    def __init__(self, approx: ApproxType, color_name: str) -> None:
        """
        Args:
            approx (ApproxType): The approximation array of the contour vertices.
            color_name (str): The name of the color (e.g., 'red', 'blue').
        """
        super().__init__(approx, color_name)