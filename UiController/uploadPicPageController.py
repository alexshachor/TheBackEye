import time
from Measurements import faceDetector as fd
from Measurements import headPose as hp
from Measurements import sleepDetector as sd
from Services import httpService as hs
import config

MSGS = {
    'FaceDetector': 'Please upload a pic with face in it.\n',
    'SleepDetector': 'Please upload a pic with eyes open.\n',
    'HeadPose': 'Pleas upload a pic when you look strata at the camera.\n'
}


def check_pic(results):
    """
    Check if the user image is a good image, if not return msg
    :param results: array of result measurements
    :return msg: return a msg for a good & bad pic.
    """
    msg = ''
    for key, val in results.items():
        if not val:
            # TODO: after measurements complete check if it work
            msg += MSGS[key]
    return msg


def upload_pic(pic):
    """
    If its a good pic send to the server. return a msg for a good & bad pic.
    :param pic: the pic from user
    :return msg: return a msg for a good & bad pic.
    """
    if config.DEBUG:
        return 'OK'
    result = {}
    measurements = [fd.FaceDetector(), sd.SleepDetector(), hp.HeadPose()]
    for measure in measurements:
        # TODO: run each algorithm in thread, then wait for their result using join
        result[str(measure)] = measure.run(pic)
    msg = check_pic(result)
    if msg == 'OK':
        # TODO: give real URL
        hs.post_image_data('somm/url', config.USER_DATA, pic)
    return msg

