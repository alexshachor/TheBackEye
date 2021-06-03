from Measurements import faceDetector as fd
from Measurements.HeadPose import headPose as hp
from Measurements import sleepDetector as sd
from Services import httpService as hs
from Core import runMeasurements as rm
import multiprocessing as mp
import config
import random

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
            msg += MSGS[key]
    return msg


def upload_pic(pics):
    """
    If its a good pics send to the server. return a msg for a good & bad pics.
    :param pics: the pics from user
    :return msg: return a dict of msgs for a good & bad pics for all images.
    """
    dict_results = mp.Manager().dict()
    processes = []
    for key, val in pics.items():
        process = mp.Process(target=run_images_checks, args=(val, dict_results, key))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
        process.close()
    flg = all(elem == '' for elem in dict_results.values())
    if flg:
        # TODO: give real URL
        for pic in pics.items():
            hs.post_image_data('somm/url', config.USER_DATA, pic)
        return 'OK'
    return dict_results


def run_images_checks(image, dict_res, i):
    if not config.DEBUG:
        measurements = [fd.FaceDetector(), sd.SleepDetector(), hp.HeadPose()]
        run_measurements = rm.RunMeasurements(measurements, None)
        result = run_measurements.run_measurement_processes(image)
    else:
        result = {'FaceDetector': bool(random.getrandbits(1)), 'SleepDetector': bool(random.getrandbits(1))
                  , 'HeadPose': bool(random.getrandbits(1))}
    msg = check_pic(result)
    dict_res[i] = msg

