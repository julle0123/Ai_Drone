# main.py

import cv2, time
from datetime import datetime
import numpy as np
from config import *
from camera import load_models, get_video_capture
from gps import read_gps_data
from s3_utils import connect_s3, upload_image
from db_utils import save_to_db
from utils import calculate_iou

# 초기화
model_car, model_plate = load_models(MODEL_CAR_PATH, MODEL_PLATE_PATH)
cap = get_video_capture()
s3 = connect_s3()
lat, lon = read_gps_data()

last_plate = None
last_bbox = None
last_time = 0
cooldown = 5
iou_thresh = 0.5

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    results = model_car(frame)
    for det in results.xyxy[0]:
        class_id = int(det[5])
        if class_id == 1:
            x1, y1, x2, y2 = map(int, det[:4])
            bbox = (x1, y1, x2, y2)
            now = time.time()

            crop = frame[y1:y2, x1:x2]
            zoom = cv2.resize(crop, (640, 480))
            res_plate = model_plate(zoom)

            detected = []
            for d in res_plate.xyxy[0]:
                id = int(d[5].item())
                name = res_plate.names[id]
                detected.append(name)
            plate_str = "_".join(detected)

            # 혼합 중복 판별
            iou = calculate_iou(last_bbox, bbox) if last_bbox else 0
            is_dup = (plate_str == last_plate and now - last_time < cooldown) or \
                     (iou > iou_thresh and now - last_time < cooldown)
            if is_dup:
                print(f"🚫 중복: {plate_str}, IoU={iou:.2f}")
                continue

            # 저장
            last_plate = plate_str
            last_bbox = bbox
            last_time = now
            timestamp = datetime.now()
            filename = f"{plate_str}_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)

            # S3
            _, encoded = cv2.imencode('.jpg', frame)
            s3_url = upload_image(s3, S3_BUCKET, f"car_images/{filename}", encoded.tobytes())

            # DB
            if s3_url:
                save_to_db(s3_url, plate_str, lat, lon, timestamp.strftime("%Y-%m-%d %H:%M:%S"))

cap.release()
cv2.destroyAllWindows()
