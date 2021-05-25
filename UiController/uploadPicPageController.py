from Measurements import faceDetector as fd
from Measurements.HeadPose import headPose as hp
from Measurements import sleepDetector as sd
from Services import httpService as hs
from Core import runMeasurements as rm
import config
import time

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
        time.sleep(3)
        return 'OK'
    measurements = [fd.FaceDetector(), sd.SleepDetector(), hp.HeadPose()]
    run_measurements = rm.RunMeasurements(measurements, None)
    result = run_measurements.run_measurement_processes(pic)
    msg = check_pic(result)
    if msg == 'OK':
        # TODO: give real URL
        hs.post_image_data('somm/url', config.USER_DATA, pic)
    return msg

