import configparser
import numpy as np
import cv2
import datetime
import csv
import os

import ImageLoader

config = configparser.ConfigParser()
config.read('Python/config.ini')

image_loader = ImageLoader.ImageLoader(config['settings']['picture_path'])
images = image_loader.load_folder_images()

for image in images:
    cv2.imshow('Image', image)
    cv2.waitKey(0)