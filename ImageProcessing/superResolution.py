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
        start = time.time()
        bicubic = cv2.resize(self.image, (self.image.shape[1], self.image.shape[0]),
                             interpolation=cv2.INTER_CUBIC)
        end = time.time()
        if config.DEBUG:
            print('[INFO] Bicubic interpolation took {:.2f} seconds'.format(end - start))
            cv2.imshow("Original", self.image)
            cv2.imshow("Bicubic", bicubic)
            cv2.imwrite('.\SavedImages\\bicubic.jpg', bicubic)
            cv2.waitKey(0)
        return bicubic

    def to_super_resolution(self):
        pass

    def init_model(self):
        pass


# For tests only.

