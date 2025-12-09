import configparser
import numpy as np
import cv2
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QLabel, QMessageBox, QFileDialog)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt

import Image_Loader as Image_Loader
import Image_Processing as Image_Processing
import Logger as Logger

config = configparser.ConfigParser()
config.read('Python/config.ini')

colors = {"red": (0, 0, 255), "green": (0, 255, 0), "blue": (255, 0, 0), "yellow": (0, 255, 255), "purple": (255, 0, 255)}

ranges = {
    "red1":   ([int(x) for x in config['pattern_recognition']['lower_red1'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_red1'].strip('[]').split(',')]),
    "red2":   ([int(x) for x in config['pattern_recognition']['lower_red2'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_red2'].strip('[]').split(',')]),
    "green":  ([int(x) for x in config['pattern_recognition']['lower_green'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_green'].strip('[]').split(',')]),
    "blue":   ([int(x) for x in config['pattern_recognition']['lower_blue'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_blue'].strip('[]').split(',')]),
    "yellow": ([int(x) for x in config['pattern_recognition']['lower_yellow'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_yellow'].strip('[]').split(',')]),
    "purple": ([int(x) for x in config['pattern_recognition']['lower_purple'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_purple'].strip('[]').split(',')])
}

image_loader = Image_Loader.Image_Loader(config['settings']['picture_path'], int(config['settings']['camera_index']))
image_processor = Image_Processing.Image_Processing(colors, ranges)
logger = Logger.Logger(config['logging']['path'])

class ShapeDetectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Object Pattern Recognizer")
        
        self.image_files = image_loader.load_folder_images()
        self.current_image_index = 0
        self.current_mode = 'camera'

        self.setup_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_frame)
        self.start_camera_mode()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        control_layout = QHBoxLayout()
        
        self.radio_camera = QRadioButton("Camera Mode")
        self.radio_camera.setChecked(True)
        self.radio_camera.toggled.connect(self.check_mode_change)
        
        self.radio_image = QRadioButton("Image Folder Mode")
        self.radio_image.toggled.connect(self.check_mode_change)
        
        control_layout.addWidget(self.radio_camera)
        control_layout.addWidget(self.radio_image)

        self.next_button = QPushButton("Next Image >>")
        self.next_button.clicked.connect(self.load_next_image)
        self.next_button.setEnabled(False)
        
        control_layout.addWidget(self.next_button)

        main_layout.addLayout(control_layout)

        self.image_label = QLabel("Waiting for camera/image data...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.image_label.setMinimumSize(640, 480) 
        
        main_layout.addWidget(self.image_label)

    def check_mode_change(self):
        if self.radio_camera.isChecked() and self.current_mode != 'camera':
            self.switch_mode('camera')
        elif self.radio_image.isChecked() and self.current_mode != 'image':
            self.switch_mode('image')

    def switch_mode(self, mode):
        self.current_mode = mode
        
        # Enable/Disable controls based on mode
        self.next_button.setEnabled(mode == 'image')
        self.folder_button.setEnabled(mode == 'image')
        
        if mode == 'camera':
            self.start_camera_mode()
        elif mode == 'image':
            self.start_image_mode()

    def start_camera_mode(self):
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start(30)

    def start_image_mode(self):
        if self.timer.isActive():
            self.timer.stop()
        self.current_image_index = 0
        self.load_current_image()

    def load_current_image(self):
        if not self.image_files:
            self.image_label.setText("No images found in the configured folder.")
            self.next_button.setEnabled(False)
            return

        if self.current_image_index < len(self.image_files):
            image = self.image_files[self.current_image_index].copy() 
            self.process_and_display(image)
        else:
            QMessageBox.information(self, "Info", "Reached the end of the image folder. Restarting loop.")
            self.current_image_index = 0 
            self.load_current_image() 

    def load_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.load_current_image()

    def update_camera_frame(self):
        if self.current_mode == 'camera':
            image = image_loader.load_camera_image()
            if image is not None:
                self.process_and_display(image)
        else:
            self.timer.stop()

    def process_and_display(self, image):
        processed_image, shapes = image_processor.process_images(image)
        logger.log_detection(shapes)
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

        height, width, channel = processed_image.shape
        bytes_per_line = 3 * width
        q_img = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShapeDetectorApp()
    window.show()
    sys.exit(app.exec())

# while True:
#     selected_mode = config['settings']['mode']
#     print("Which mode do want to select:\n[0] Default\n[1] Image\n[2] Camera")
#     selection = int(input())
#     if selection == 0:
#         pass
#     elif selection == 1:
#         selected_mode = 'image'
#     elif selection == 2:
#         selected_mode = 'camera'
#     else:
#         print("Invalid selection, defaulting to 'image' mode.")
    
#     if selected_mode == 'camera':
#         print("Starting camera mode. Press 'q' to quit.")
#         while True:
#             image = image_loader.load_camera_image()
#             image, shapes = image_processor.process_images(image)
#             logger.log_detection(shapes)
#             cv2.imshow('Image', image)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#     else:
#         print("Starting image mode. Press any key to proceed through images.")
#         images = image_loader.load_folder_images()

#         for image in images:
#             image, shapes = image_processor.process_images(image)
#             logger.log_detection(shapes)
#             cv2.imshow('Image', image)
#             cv2.waitKey(0)
#     cv2.destroyAllWindows() 