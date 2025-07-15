# camera.py

import cv2
import torch

def load_models(car_model_path, plate_model_path):
    model_car = torch.hub.load('ultralytics/yolov5', 'custom', path=car_model_path)
    model_plate = torch.hub.load('ultralytics/yolov5', 'custom', path=plate_model_path)
    return model_car, model_plate

def get_video_capture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    return cap
