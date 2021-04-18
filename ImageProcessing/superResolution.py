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
            time.sleep(5)
        return bicubic

    def to_super_resolution(self):
        model = self.init_model()
        start = time.time()
        scaled_image = model.upsample(self.image)
        end = time.time()
        if config.DEBUG:
            print("[INFO] width: {}, height: {} - Before scaling".format(self.image.shape[1], self.image.shape[0]))
            print("[INFO] width: {}, height: {} - After scaling".format(scaled_image.shape[1], scaled_image.shape[0]))
            print('[INFO] Super resolution interpolation took {:.2f} seconds'.format(end - start))
            cv2.imshow("Original", self.image)
            cv2.imshow("Super Resolution", scaled_image)
            cv2.imwrite('.\SavedImages\\superRes.jpg', scaled_image)
            time.sleep(5)
        return scaled_image

    def init_model(self):
        model_file = self.models[self.quality]
        self.model_name = model_file.split('_')[0].lower()
        scale = self.model_scale[self.quality]
        super_resolution = cv2.dnn_superres.DnnSuperResImpl_create()
        super_resolution.readModel(self.path + model_file)
        super_resolution.setModel(self.model_name, scale)
        return super_resolution


def for_tests_only():
    image = cv2.imread('.\SavedImages\\butterfly.png')
    SuperResolution(image, 'HIGH').to_bicubic()
    SuperResolution(image, 'HIGH').to_super_resolution()


if __name__ == '__main__':
    for_tests_only()

