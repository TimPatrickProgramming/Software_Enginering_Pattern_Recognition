import cv2
import os
import numpy as np
from typing import Optional

class Image_Loader:
    """
    Manages image data acquisition, either from a folder path or a live camera feed.
    """
    def __init__(self, image_path:str, select_camera:int) -> None:
        """
        Initializes the Image_Loader.

        Args:
            image_path (str): Path to the folder containing image files for IMAGE mode.
            select_camera (int): Index of the camera device (e.g., 0 for default).
        """
        self.image_path = image_path
        self.cam = cv2.VideoCapture(select_camera)

    def load_folder_images(self) -> list[np.ndarray]:
        """
        Loads all image files (png, jpg, jpeg) from the configured folder path.

        Returns:
            list: A list of OpenCV image frames (numpy arrays).
        """
        images = []
        if not os.path.isdir(self.image_path):
            return []
        for filename in sorted(os.listdir(self.image_path)):
            img_path = os.path.join(self.image_path, filename)
            if os.path.isfile(img_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = cv2.imread(img_path)
                if img is not None:
                    images.append(img)
        return images
    
    def load_camera_image(self) -> Optional[np.ndarray]:
        """
        Captures the current frame from the initialized camera device.

        Returns:
            numpy.ndarray or None: The captured frame or None if capture failed.
        """
        ret, frame = self.cam.read()
        if ret:
            return frame
        else:
            return None
    
    
    def release_camera(self) -> None:
        """
        Releases the camera hardware resource, freeing it for other applications.
        """
        self.cam.release()