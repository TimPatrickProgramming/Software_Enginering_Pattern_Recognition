import cv2
import os

class Image_Loader:
    def __init__(self, image_path, select_camera):
        self.image_path = image_path
        self.cam = cv2.VideoCapture(select_camera)

    def load_folder_images(self):
        images = []
        for filename in os.listdir(self.image_path):
            img_path = os.path.join(self.image_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
        return images
    
    def load_camera_image(self):
        ret, frame = self.cam.read()
        if ret:
            return frame
        else:
            return None