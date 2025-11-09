import configparser
import numpy as np
import cv2
import datetime
import csv
import os

import Image_Loader as Image_Loader
import Image_Processing as Image_Processing

config = configparser.ConfigParser()
config.read('Python/config.ini')

colors = {"red": (0, 0, 255), "green": (0, 255, 0), "blue": (255, 0, 0), "yellow": (0, 255, 255), "purple": (255, 0, 255)}

ranges = {
    "red":    ([int(x) for x in config['pattern_recognition']['lower_red'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_red'].strip('[]').split(',')]),
    "green":    ([int(x) for x in config['pattern_recognition']['lower_green'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_green'].strip('[]').split(',')]),
    "blue":   ([int(x) for x in config['pattern_recognition']['lower_blue'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_blue'].strip('[]').split(',')]),
    "yellow": ([int(x) for x in config['pattern_recognition']['lower_yellow'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_yellow'].strip('[]').split(',')]),
    "purple": ([int(x) for x in config['pattern_recognition']['lower_purple'].strip('[]').split(',')],
               [int(x) for x in config['pattern_recognition']['upper_purple'].strip('[]').split(',')])
}

image_loader = Image_Loader.Image_Loader(config['settings']['picture_path'])
images = image_loader.load_folder_images()
image_processor = Image_Processing.Image_Processing(colors, ranges)

for image in images:
    image = image_processor.process_images(image)

    cv2.imshow('Image', image)
    cv2.waitKey(0)