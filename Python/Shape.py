from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class for geometric shapes."""

    # @abstractmethod
    # def area(self):
    #     pass


class Triangle(Shape):
    def __init__(self, approx, color_name):
        self.approx = approx
        self.color_name = color_name


class Rectangle(Shape):
    def __init__(self, approx, color_name):
        self.approx = approx
        self.color_name = color_name


class Square(Shape):
    def __init__(self, approx, color_name):
        self.approx = approx
        self.color_name = color_name


class Circle(Shape):
    def __init__(self, approx, color_name):
        self.approx = approx
        self.color_name = color_name