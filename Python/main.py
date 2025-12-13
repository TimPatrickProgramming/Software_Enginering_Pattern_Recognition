import configparser
import numpy as np
import cv2
import sys

import Image_Loader as Image_Loader
import Image_Processing as Image_Processing
import Logger as Logger
import ShapeDetectorApp as ShapeDetectorApp

from PyQt6.QtWidgets import QApplication

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

def run_console_mode(selected_input_mode:str) -> None:
    """
    Runs the console-based mode with OpenCV windows. 
    It loops through camera or image mode until the user selects 'Quit'.
    """
    while True:               
        if selected_input_mode == 'camera':
            print("Starting camera mode. Press 'q' to quit.")
            while True:
                image = image_loader.load_camera_image()
                image, shapes = image_processor.process_image(image)
                logger.log_detection(shapes)
                cv2.imshow('Image', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            print("Starting image mode. Press any key to proceed through images.")
            images = image_loader.load_folder_images()

            for image in images:
                image, shapes = image_processor.process_image(image)
                logger.log_detection(shapes)
                cv2.imshow('Image', image)
                cv2.waitKey(0)

        cv2.destroyAllWindows() 
        
        print("Which mode do want to select:\n[0] Default\n[1] Image\n[2] Camera\n[3] Quit")
        selection = int(input())
        if selection == 0:
            pass
        elif selection == 1:
            selected_input_mode = 'image'
        elif selection == 2:
            selected_input_mode = 'camera'
        elif selection == 3:
            break
        else:
            print("Invalid selection, defaulting to 'image' mode.")
            selected_input_mode = config['settings']['mode']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_mode = sys.argv[1].upper()
        if run_mode != 'CONSOLE' and run_mode != 'GUI':
            run_mode = config['settings']['run_mode']
    else:
        run_mode = config['settings']['run_mode']    
        
    if run_mode == 'GUI':
        app = QApplication(sys.argv)
        window = ShapeDetectorApp.ShapeDetectorApp(image_loader, image_processor, logger)
        window.show()
        sys.exit(app.exec())

    else:
        if len(sys.argv) > 2:
            input_mode = sys.argv[2].upper()
            if input_mode == 'IMAGE':
                selected_input_mode = 'image'
            elif input_mode == 'CAMERA':
                selected_input_mode = 'camera'
            else:
                print("Invalid mode argument, defaulting to config setting.")
                selected_input_mode = config['settings']['mode']
        else:
            selected_input_mode = config['settings']['mode']
        run_console_mode(selected_input_mode)