import numpy as np
import cv2

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QLabel, QMessageBox, QFileDialog)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt

class ShapeDetectorApp(QWidget):
    def __init__(self, image_loader, image_processor, logger):
        super().__init__()
        self.image_loader = image_loader
        self.image_processor = image_processor
        self.logger = logger

        self.setWindowTitle("Object Pattern Recognizer")
        
        self.image_files = self.image_loader.load_folder_images()
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

        self.folder_button = QPushButton("Select Image Folder")
        self.folder_button.clicked.connect(self.select_folder)
        control_layout.addWidget(self.folder_button)
        
        control_layout.addStretch(1)

        self.next_button = QPushButton("Next Image >>")
        self.next_button.clicked.connect(self.load_next_image)
        self.next_button.setEnabled(False)
        
        control_layout.addWidget(self.next_button)

        main_layout.addLayout(control_layout)

        self.image_label = QLabel("Waiting for camera/image data...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.image_label.setMinimumSize(640, 480) 
        
        main_layout.addWidget(self.image_label)

    def select_folder(self):        
        current_path = self.image_loader.image_path
        
        new_path = QFileDialog.getExistingDirectory(self, "Select directory to load images from", current_path)
        
        if new_path:
            self.image_loader.image_path = new_path
            
            self.image_files = self.image_loader.load_folder_images()
            self.current_image_index = 0
            
            QMessageBox.information(self, "Folder Updated", 
                                    f"New folder selected: {new_path}\n{len(self.image_files)} images loaded.")

            if self.current_mode == 'image':
                self.load_current_image()

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
            image = self.image_loader.load_camera_image()
            if image is not None:
                self.process_and_display(image)
        else:
            self.timer.stop()

    def process_and_display(self, image):
        processed_image, shapes = self.image_processor.process_images(image)
        self.logger.log_detection(shapes)
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def closeEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
        self.image_loader.release_camera()
        event.accept()