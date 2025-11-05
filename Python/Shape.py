from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class for geometric shapes."""

    @abstractmethod
    def area(self):
        pass


class Triangle(Shape):
    def __init__(self, approx):
        self.approx = approx


class Rectangle(Shape):
    def __init__(self, approx):
        self.approx = approx


class Square(Shape):
    def __init__(self, approx):
        self.approx = approx


class Circle(Shape):
    def __init__(self, approx):
        self.approx = approx