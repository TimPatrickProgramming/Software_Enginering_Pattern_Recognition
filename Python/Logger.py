import csv
import os
import cv2
import datetime

class Logger:
    """
    Handles logging of detected shapes (type and color) to a CSV file.
    """
    DEBOUNCE_DISTANCE: int = 100   # Pixels: Minimum movement required to log the shape again

    def __init__(self, log_path:str) -> None:
        """
        Initializes the Logger with the target log file path.

        Args:
            log_path (str): The path to the CSV file where detection data will be logged.
        """
        self.log_path = log_path
        self.last_detections = {}  # Stores {key: (last_x, last_y)}

    def log_detection(self, shapes:list) -> None:
        """
        Writes the timestamp, shape type, and color name for each detected shape
        to the configured CSV log file.

        Args:
            shapes (list[Shape]): A list of Shape objects detected in the current frame/image.
        """
        now = datetime.datetime.now()
        current_frame_detections = {}

        try:
            with open(self.log_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)

                if csvfile.tell() == 0: 
                    writer.writerow(["Timestamp                  | ShapeType | ColorName"])

                for shape in shapes:
                    M = cv2.moments(shape.approx)
                    if M["m00"] != 0:
                        center_x = int(M["m10"] / M["m00"])
                        center_y = int(M["m01"] / M["m00"])
                    else:
                        continue  # Skip logging if center cannot be calculated

                    current_pos = (center_x, center_y)
                    shape_key = f"{shape.__class__.__name__}_{shape.color_name}"
                    should_log = True
                    last_pos = self.last_detections.get(shape_key)

                    if last_pos:
                        dist_sq = (current_pos[0] - last_pos[0]) ** 2 + (current_pos[1] - last_pos[1]) ** 2
                        if dist_sq < self.DEBOUNCE_DISTANCE ** 2:
                            should_log = False

                    if should_log:
                        class_name = shape.__class__.__name__.ljust(9, ' ')
                        writer.writerow([f"{now} | {class_name} | {shape.color_name}"])
                    
                    current_frame_detections[shape_key] = current_pos

                self.last_detections = current_frame_detections

        except Exception as e:
            print(f"Unexpected logging error: {e}")