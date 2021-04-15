import cv2
import time
import config


class SuperResolution:
    def __init__(self, img, quality):
        self.image = img
        self.quality = quality.upper() if quality.upper() in ['LOW', 'MEDIUM', 'HIGH'] else 'LOW'
        self.path = '.\Models\\'
        self.models = {'LOW': 'FSRCNN_x3.pb', 'MEDIUM': 'ESPCN_x4.pb', 'MediumGPU': 'EDSR_x4.pb',
                       'HIGH': 'LapSRN_x8.pb'}
        self.model_name = ''
        self.model_scale = {'LOW': 3, 'MEDIUM': 4, 'HIGH': 8}

    def to_bicubic(self):
        pass

    def to_super_resolution(self):
        pass

    def init_model(self):
        pass


# For tests only.

