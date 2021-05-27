import cv2
import numpy as np
from PIL import Image
import config


class FaceTraining:

    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier('.\Models\haarcascade_frontalface_default.xml')
        self.image_paths = ['.\Images\\1.jpg', '.\Images\\2.jpg', '.\Images\\3.jpg',
                            '.\Images\\4.jpg', '.\Images\\5.jpg']
        print('[INFO] Training faces. It will take a few seconds.') if config.DEBUG else None
        self.faces, self.ids = self.__get_images_labels()
        self.__train()
        print('[INFO] faces trained. Exiting Program') if config.DEBUG else None

    def __get_images_labels(self):
        face_samples = []
        id_s = []
        for path in self.image_paths:
            # convert it to grayscale
            img = Image.open(path).convert('L')
            img_numpy = np.array(img, 'uint8')
            faces = self.detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y + h, x:x + w])
                id_s.append(1)
        return face_samples, id_s

    def __train(self):
        pass


def for_tests_only():
    pass


if __name__ == "__main__":
    for_tests_only()
