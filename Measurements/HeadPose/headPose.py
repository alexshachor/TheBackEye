import cv2
import config
from Measurements import abstractMeasurement as am
from Services import loggerService
import warnings
import numpy as np
import torch
import math
from torchvision import transforms
import cv2
from dectect import AntiSpoofPredict

from pfld.pfld import PFLDInference

warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class HeadPose(am.AbstractMeasurements):

    def __init__(self):
        """
        initialize the parent class.
        """
        am.AbstractMeasurements.__init__(self)

    def run(self, frame, dict_results):
        """
        run the head pose algorithm on the given frame
        :param frame: frame to process.
        :param dict_results: a dictionary which the result will be put there
        :return: pair of key = 'HeadPose',
        value = True if the face is looking toward the screen and False otherwise.
            """
        run_result = {repr(self): False}
        try:
            point_dict = get_point_dict(frame)

            point1 = [get_num(point_dict, 1, 0), get_num(point_dict, 1, 1)]
            point31 = [get_num(point_dict, 31, 0), get_num(point_dict, 31, 1)]
            point51 = [get_num(point_dict, 51, 0), get_num(point_dict, 51, 1)]
            crossover51 = get_intersection(point51, [point1[0], point1[1], point31[0], point31[1]])

            # get yaw, pitch and roll measures
            yaw = get_yaw(point1, point31, crossover51)
            pitch = get_pitch(point51, crossover51)
            roll = get_roll(point_dict)

            run_res = True
            is_looking = {'yaw': True, 'pitch': True, 'roll': True}
            # TODO: change it to take boundaries from configuration file
            if yaw > 10 or yaw < -10:
                run_res = is_looking['yaw'] = False
            if pitch > 20 or pitch < 4:
                run_res = is_looking['pitch'] = False

            if config.DEBUG:
                cv2.putText(frame, f"Yaw(degree): {yaw}", (30, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Pitch(degree): {pitch}", (30, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0),
                            2)
                cv2.putText(frame, f"Roll(degree): {roll}", (30, 150), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0),
                            2)
                cv2.putText(frame, f"look  {is_looking['yaw']}", (30, 200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                            (0, 255, 0), 2)
                cv2.putText(frame, f"look  {is_looking['pitch']}", (30, 250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                            (0, 255, 0), 2)
                cv2.putText(frame, f"look  {is_looking['roll']}", (30, 300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                            (0, 255, 0), 2)

                video_writer = get_video_writer()
                video_writer.write(frame)

            # if results.multi_face_landmarks:
            #     # face has been detected
            #     run_result[repr(self)] = True
            #
            #     # if config.DEBUG:
            #     #     self.draw_annonations(image, results)



            dict_results.update(run_result)

        except Exception as e:
            # write error to log file
            loggerService.get_logger().error(str(e))

    def __repr__(self):
        return 'HeadPose'

def get_num(point_dict, name, axis):
    num = point_dict.get(f'{name}')[axis]
    num = float(num)
    return num


def get_intersection(point, line):
    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]

    x3 = point[0]
    y3 = point[1]

    k1 = (y2 - y1) * 1.0 / (x2 - x1)
    b1 = y1 * 1.0 - x1 * k1 * 1.0
    k2 = -1.0 / k1
    b2 = y3 * 1.0 - x3 * k2 * 1.0
    x = (b2 - b1) * 1.0 / (k1 - k2)
    y = k1 * x * 1.0 + b1 * 1.0
    return [x, y]


def get_distance(point_1, point_2):
    x1 = point_1[0]
    y1 = point_1[1]
    x2 = point_2[0]
    y2 = point_2[1]
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance


def get_frame_cropped(frame):
    height, width = frame.shape[:2]
    # TODO: should replace 0 with device id
    model_test = AntiSpoofPredict(0)
    image_bbox = model_test.get_bbox(frame)

    x1 = image_bbox[0]
    y1 = image_bbox[1]
    x2 = image_bbox[0] + image_bbox[2]
    y2 = image_bbox[1] + image_bbox[3]
    w = x2 - x1
    h = y2 - y1

    size = int(max([w, h]))
    cx = x1 + w / 2
    cy = y1 + h / 2
    x1 = cx - size / 2
    x2 = x1 + size
    y1 = cy - size / 2
    y2 = y1 + size

    dx = max(0, -x1)
    dy = max(0, -y1)
    x1 = max(0, x1)
    y1 = max(0, y1)

    edx = max(0, x2 - width)
    edy = max(0, y2 - height)
    x2 = min(width, x2)
    y2 = min(height, y2)

    cropped = frame[int(y1):int(y2), int(x1):int(x2)]
    if dx > 0 or dy > 0 or edx > 0 or edy > 0:
        cropped = cv2.copyMakeBorder(cropped, dy, edy, dx, edx, cv2.BORDER_CONSTANT, 0)

    return cropped


def get_point_dict(frame):
    # get cropped
    cropped = get_frame_cropped(frame)
    cropped = cv2.resize(cropped, (112, 112))

    # get input
    transform = transforms.Compose([transforms.ToTensor()])
    input = cv2.resize(cropped, (112, 112))
    input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
    input = transform(input).unsqueeze(0).to(device)

    # get landmark
    plfd_backbone = init_plfd_backbone()
    _, landmarks = plfd_backbone(input)
    pre_landmark = landmarks[0]
    pre_landmark = pre_landmark.cpu().detach().numpy().reshape(-1, 2) * [112, 112]

    point_dict = {}
    i = 0
    for (x, y) in pre_landmark.astype(np.float32):
        point_dict[f'{i}'] = [x, y]
        i += 1

    return point_dict


def init_plfd_backbone():
    # TODO: take path from configuration file, change it to the true relative path
    checkpoint = torch.load("./checkpoint/snapshot/checkpoint.pth.tar", map_location=device)
    plfd_backbone = PFLDInference().to(device)
    plfd_backbone.load_state_dict(checkpoint['plfd_backbone'])
    plfd_backbone.eval()
    plfd_backbone = plfd_backbone.to(device)
    return plfd_backbone


def get_yaw(point1, point31, crossover51):
    yaw_mean = get_distance(point1, point31) / 2
    yaw_right = get_distance(point1, crossover51)
    yaw = (yaw_mean - yaw_right) / yaw_mean
    yaw = int(yaw * 71.58 + 0.7037)
    return yaw


def get_pitch(point51, crossover51):
    pitch_dis = get_distance(point51, crossover51)
    if point51[1] < crossover51[1]:
        pitch_dis = -pitch_dis
    pitch = int(1.497 * pitch_dis + 18.97)
    return pitch


def get_roll(point_dict):
    roll_tan = abs(get_num(point_dict, 60, 1) - get_num(point_dict, 72, 1)) / abs(
        get_num(point_dict, 60, 0) - get_num(point_dict, 72, 0))
    roll = math.atan(roll_tan)
    roll = math.degrees(roll)
    if get_num(point_dict, 60, 1) > get_num(point_dict, 72, 1):
        roll = -roll
    roll = int(roll)
    return roll


def get_video_writer():
    # TODO: get video capture from configuration file
    video_capture = cv2.VideoCapture(1)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # print("fps:", fps, "size:", size)
    # TODO: get file path from configuration file
    video_writer = cv2.VideoWriter("./video/result.avi", cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps, size)
    return video_writer


