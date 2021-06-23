import cv2
import time
import os
import config


class SuperResolution:

    def __init__(self, img, quality, debug=False):
        """
        initialize params for this class.
        :param: img: the image to improve
        :param: quality: in which quality the result pic should be
        """
        self.image = img
        self.quality = quality.upper() if quality.upper() in ['LOW', 'MEDIUM', 'HIGH'] else 'LOW'
        self.path = '.\Models\\'
        self.models = {'LOW': 'FSRCNN_x3.pb', 'MEDIUM': 'ESPCN_x4.pb', 'MediumGPU': 'EDSR_x4.pb',
                       'HIGH': 'LapSRN_x8.pb'}
        self.model_name = ''
        self.model_scale = {'LOW': 3, 'MEDIUM': 4, 'HIGH': 8}
        self.debug = debug

    def to_bicubic(self):
        """
        a minor improvement to a picture, take a very sort time.
        :return: bicubic: a bicubic improvement image
        """
        start = time.time()
        bicubic = cv2.resize(self.image, (self.image.shape[1], self.image.shape[0]),
                             interpolation=cv2.INTER_CUBIC)
        end = time.time()
        if self.debug:
            print('[INFO] Bicubic interpolation took {:.2f} seconds'.format(end - start))
            cv2.imshow("Original", self.image)
            cv2.imshow("Bicubic", bicubic)
            cv2.imwrite('.\SavedImages\\bicubic.jpg', bicubic)
            cv2.waitKey(0)
        return bicubic

    def to_super_resolution(self):
        """
        use the heavy tools to improve image by the expropriate models.
        :return: scaled_image: depend on what the quality that the user
        ask for
        """
        model = self.init_model()
        start = time.time()
        scaled_image = model.upsample(self.image)
        end = time.time()
        if self.debug:
            print("[INFO] width: {}, height: {} - Before scaling".format(self.image.shape[1], self.image.shape[0]))
            print("[INFO] width: {}, height: {} - After scaling".format(scaled_image.shape[1], scaled_image.shape[0]))
            print('[INFO] Super resolution interpolation took {:.2f} seconds'.format(end - start))
            cv2.imshow("Original", self.image)
            cv2.imshow("Super Resolution", scaled_image)
            cv2.imwrite('.\SavedImages\\superRes.jpg', scaled_image)
            cv2.waitKey(0)
        return scaled_image

    def init_model(self):
        """
        this func will init model by the asked quality
        """
        model_file = self.models[self.quality]
        self.model_name = model_file.split('_')[0].lower()
        scale = self.model_scale[self.quality]
        super_resolution = cv2.dnn_superres.DnnSuperResImpl_create()
        script_dir = os.path.dirname(__file__)
        super_resolution.readModel(os.path.join(script_dir, "Models/" + model_file))
        super_resolution.setModel(self.model_name, scale)
        return super_resolution


def for_tests_only():
    """
    A test func to this page only..
    """
    image = cv2.imread('.\SavedImages\\butterfly.png')
    SuperResolution(image, 'LOW').to_bicubic()
    SuperResolution(image, 'MEDIUM', True).to_super_resolution()


if __name__ == '__main__':
    for_tests_only()

