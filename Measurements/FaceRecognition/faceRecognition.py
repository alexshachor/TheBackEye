import cv2
from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config
import os


class FaceRecognition(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class, model, threshold
        """
        am.AbstractMeasurement.__init__(self)
        self.__recognizer = cv2.face.LBPHFaceRecognizer_create()
        script_dir = os.path.dirname(__file__)
        self.__path = os.path.join(script_dir, "Model/haarcascade_eye_tree_eyeglasses.xml")
        self.__recognizer.read(os.path.join(script_dir, 'Models/trainer.yml'))
        self.__cascade_path = os.path.join(script_dir, 'Models/haarcascade_frontalface_default.xml')
        self.__face_cascade = cv2.CascadeClassifier(self.__cascade_path)
        self.__threshold = 45
        self.__id = 0
        # names related to ids - example, Shalom: id=3, this line used only for testing
        self.__names = ['None', config.USER_DATA['USERNAME'], 'Alex', 'Shalom', 'L', 'Z', 'W']

    def run(self, frame, dict_results):
        """
        report if we detect the student face. if yes
        update the dict_results to false else true.
        :param frame: frame to process
        :param dict_results: a dictionary which the result will be put there
        """
        am.AbstractMeasurement.run(self, frame, dict_results)
        result = {repr(self): False}
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.__get_faces(frame, gray)
            for (x, y, w, h) in faces:
                self.__id, confidence = self.__recognizer.predict(gray[y:y + h, x:x + w])
                # check if confidence is less them 100, zero is perfect confidence
                print(round(100 - confidence)) if config.DEBUG else None
                if confidence < 100:
                    if round(100 - confidence) >= self.__threshold:
                        result[repr(self)] = True
                if config.DEBUG:
                    self.run_debug(frame, x, y, h, w, confidence)
            dict_results.update(result)
        except Exception as e:
            ls.get_logger().error(
                f'Failed in face recognition, due to: {str(e)}')

    def __repr__(self):
        """
        :return: the name of the measurement.
        """
        return 'FaceRecognition'

    def __get_faces(self, frame, gray):
        """
        run the model and return the faces it detected.
        :param frame: frame to process
        :param gray: cvt - the frame in gray color
        :return: faces: the faces it detected
        """
        faces = self.__face_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5,
            minSize=(int(0.1 * frame.shape[1]), int(0.1 * frame.shape[0])),
        )
        return faces

    def run_debug(self, img, x, y, h, w, confidence):
        """
        in debug mode, put txt & boxes on the image we examined
        :param img: the image to put the txt on
        :param x: the x point to draw on
        :param y: the y point to draw on
        :param h: the height of the rectangle to draw
        :param w: the width of the rectangle to draw
        :param confidence: the confidence of the result to draw
        """
        name = str(self.__names[self.__id]) if confidence < 100 else 'unknown'
        confidence = "  {0}%".format(round(100 - confidence))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)


def for_tests_only():
    """
    this function is used only for tests.
    open the camera and start testing
    """
    x = FaceRecognition()
    dict_res = {}
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # set video width
    cam.set(3, 640)
    # set video height
    cam.set(4, 480)
    while True:
        ret, img = cam.read()
        x.run(img, dict_res)
        print(dict_res[x.__repr__()])
        cv2.imshow('camera', img)
        # Press 'ESC' for exiting video
        k = cv2.waitKey(10) & 0xff
        if cv2.waitKey(10) & 0xff == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    for_tests_only()
