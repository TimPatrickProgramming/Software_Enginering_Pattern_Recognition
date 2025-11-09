import csv
import os
import datetime

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path

    def log_detection(self, shapes):
        now = datetime.datetime.now()
        for shape in shapes:
            data = [now, shape.__class__.__name__, shape.color_name]
            with open(self.log_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(data)