import csv
import os
import datetime

class Logger:
    """
    Handles logging of detected shapes (type and color) to a CSV file.
    """
    def __init__(self, log_path:str) -> None:
        """
        Initializes the Logger with the target log file path.

        Args:
            log_path (str): The path to the CSV file where detection data will be logged.
        """
        self.log_path = log_path

    def log_detection(self, shapes:list) -> None:
        """
        Writes the timestamp, shape type, and color name for each detected shape
        to the configured CSV log file.

        Args:
            shapes (list): A list of Shape objects detected in the current frame/image.
        """
        now = datetime.datetime.now()
        for shape in shapes:
            class_name = shape.__class__.__name__.ljust(9, ' ')
            data = [f"{now} | {class_name} | {shape.color_name}"]
            with open(self.log_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(data)