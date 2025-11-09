import cv2
import numpy as np
import configparser

import Shape

config = configparser.ConfigParser()
config.read('Python/config.ini')

font = getattr(cv2, config['settings']['font'])
fontscale = float(config['settings']['fontscale'])
thickness = int(config['settings']['thickness'])
text_color = eval(config['settings']['text_color'])

class Visualisation:
    @staticmethod
    def draw_contours(imageFrame, shapes):
        for shape in shapes:
            # Get min from first and second column
            min_x = np.min(shape.approx[:, 0])
            min_y = np.min(shape.approx[:, 1])
            cv2.drawContours(imageFrame, [shape.approx], 0, (0,255,0), 2)
            cv2.putText(
                imageFrame,
                f"{shape.color_name} {shape.__class__.__name__}",
                (int(min_x), int(min_y) - 5),
                font,
                fontscale,
                text_color,
                thickness,
                cv2.LINE_AA, 
                False
            ) 
        return imageFrame