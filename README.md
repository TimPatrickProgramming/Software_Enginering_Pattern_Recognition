# Software Engineering Pattern Recognition Project

## Purpose of this Project

This project implements a Python-based computer vision application for real-time pattern and color recognition. The system can identify geometric shapes (circles, rectangles, squares, and triangles) and their associated colors (red, green, blue, yellow and violet) from visual input.

### Key Features

- **Dual Input Modes**: Process images from a live camera feed or from a folder of static images
- **Shape Detection**: Recognizes circles, rectangles, squares, and triangles using contour approximation
- **Color Recognition**: Identifies five base colors (red, green, blue, yellow and violet) through HSV color space filtering
- **Visual Feedback**: Highlights detected patterns directly on the processed images
- **Automated Logging**: Records all detections with their shape type and color to a CSV file
- **Configurable Settings**: Customize color ranges and detection parameters via an external configuration file

