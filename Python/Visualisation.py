import cv2
import numpy as np
import configparser

import Shape

config = configparser.ConfigParser()
config.read('Python/config.ini')

class Visualisation:
    def draw_contours(self, imageFrame, shapes):
        for shape in shapes:
            # Get min from first and second column
            min_x = np.min(shape.approx[:, 0])
            min_y = np.min(shape.approx[:, 1])
            cv2.drawContours(imageFrame, [shape.approx], 0, (0,255,0), 2)
            cv2.putText(imageFrame, f"{shape.color_name} {shape.__class__}", (min_x, min_y-5), 
                        config['settings']['font'], config['settings']['fontscale'], 
                        config['settings']['text_color'], config['settings']['thickness'], cv2.LINE_AA, False)
        return imageFrame