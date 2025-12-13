import numpy as np
import cv2
from typing import Dict, Tuple, List, Any

import Shape as Shape
import Visualisation as Visualisation

class Image_Processing:
    """
    Contains the logic for image segmentation (color filtering) and geometric
    shape detection (contour analysis).
    """
    def __init__(self, colors:Dict[str, Tuple[int, int, int]], ranges:Dict[str, Tuple[List[int], List[int]]]) -> None:
        """
        Initializes the Image_Processing component.

        Args:
            colors (Dict[str, Tuple[int, int, int]]): Dictionary mapping color names to BGR tuples.
            ranges (Dict[str, Tuple[List[int], List[int]]]): Dictionary mapping HSV range keys (e.g., 'green') to (lower_hsv, upper_hsv) tuples.
        """
        self.colors = colors
        self.ranges = ranges

    def process_image(self, image: np.ndarray) -> Tuple[np.ndarray, List[Shape.Shape]]:
        """
        Converts the image to HSV, applies color masks, finds contours, classifies shapes,
        and draws results.

        Args:
            image (np.ndarray): The input BGR image frame.

        Returns:
            Tuple[np.ndarray, List[Shape]]: (output_image, shapes), where output_image is the image with contours
                   drawn, and shapes is a list of detected Shape objects.
        """
        hsvFrame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        shapes = []
        for color_name, (lower, upper) in self.ranges.items():
            lower_np = np.array(lower, np.uint8)
            upper_np = np.array(upper, np.uint8)
            mask = cv2.inRange(hsvFrame, lower_np, upper_np)
            if color_name.startswith("red"):
                color_name = "red"
            # detect contours / shapes
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                approx = cv2.approxPolyDP(contour,0.04*cv2.arcLength(contour,True),True)
                shape = len(approx)
                approx = approx.reshape(-1, 2)
                area = cv2.contourArea(contour)
                if area > 300:
                    # Get the minimum area rectangle
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)     # Get 4 corner points
                    #box = np.int0(box)            # Convert to int
                    box = box.astype(int)
                    # Initialize shape_selector
                    if shape == 3:
                        shapes.append(Shape.Triangle(approx, color_name))
                    elif shape == 4:
                        a = np.sqrt((box[0,0]-box[1,0])**2 + (box[0,1]-box[1,1])**2)
                        b = np.sqrt((box[1,0]-box[2,0])**2 + (box[1,1]-box[2,1])**2)
                        if np.abs(a-b) < 10:
                            shapes.append(Shape.Square(approx, color_name))
                        else:
                            shapes.append(Shape.Rectangle(approx, color_name))
                    elif shape > 6:
                        shapes.append(Shape.Circle(approx, color_name))
        visualisation = Visualisation.Visualisation()
        output_image = visualisation.draw_contours(image, shapes)
        return output_image, shapes
