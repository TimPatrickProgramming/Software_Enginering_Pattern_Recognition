import cv2
import os

class ImageLoader:
    def __init__(self, image_path):
        self.image_path = image_path

    def load_folder_images(self):
        images = []
        for filename in os.listdir(self.image_path):
            img_path = os.path.join(self.image_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
        return images