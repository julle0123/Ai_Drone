import cv2
import torch
import time
import os
import numpy as np
import boto3
from sshtunnel import SSHTunnelForwarder
import pymysql
from datetime import datetime
import serial

# Load YOLO models
model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/jetson/yolov5/num.pt')
model2 = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/jetson/yolov5/best.pt')

# S3 and RDS configuration
bucket_name = "capstone2024s3"
ssh_host = '43.203.251.33'
ssh_port = 22
ssh_username = 'ubuntu'
ssh_private_key_path = '/home/jetson/capstoneKEY.pem'

rds_host = 'capstone2024.cjygcowwu2k3.ap-northeast-2.rds.amazonaws.com'
rds_port = 3306
rds_username = 'admin'
rds_password = 'capstone2024'
rds_database = 'capstone2024'

# S3 connection function
def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="AKIA************",
            aws_secret_access_key="************************************"
        )
        print("S3 connected successfully!")
        return s3
    except Exception as e:
        print("S3 connection error:", e)
        return None

def upload_image_to_s3(s3, image_data, bucket_name, s3_file_key):
    try:
        s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=image_data, ContentType='image/jpeg')
        print(f"Image successfully uploaded to: {bucket_name}/{s3_file_key}")
        return f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{s3_file_key}"
    except Exception as e:
        print("Image upload failed:", e)
        return None

# NMEA 데이터에서 위도와 경도 추출
def parse_nmea_data(nmea_sentence):
    try:
        parts = nmea_sentence.split(',')
        if parts[0] == "$GPGGA":
            lat = parts[2]
            lat_dir = parts[3]
            lon = parts[4]
            lon_dir = parts[5]
            latitude = convert_to_decimal_degrees(lat, lat_dir)
            longitude = convert_to_decimal_degrees(lon, lon_dir)
            return latitude, longitude
        return None, None
    except Exception as e:
        print(f"Error parsing NMEA data: {e}")
        return None, None

# 도분초 → 십진수
def convert_to_decimal_degrees(coord, direction):
    degrees = float(coord[:2])
    minutes = float(coord[2:]) / 60
    decimal_degrees = degrees + minutes
    if direction == 'S' or direction == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees

# GPS 데이터 읽기
def read_gps_data():
    gps_port = '/dev/ttyTHS1'
    gps_baudrate = 57600
    try:
        with serial.Serial(gps_port, gps_baudrate, timeout=1) as ser:
            while True:
                nmea_sentence = ser.readline().decode('utf-8', errors='replace').strip()
                latitude, longitude = parse_nmea_data(nmea_sentence)
                if latitude and longitude:
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                    return latitude, longitude
    except Exception as e:
        print(f"GPS data read error: {e}")
        return None, None

# 메인 실행
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 원본 해상도 설정
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

s3 = s3_connection()
latitude, longitude = read_gps_data()
fixed_size = (640, 480)

frame_skip = 2
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    # 모델 2 객체 감지
    results2 = model2(frame)

    # 모델 2결과 시각화
    original_frame = frame.copy()
    annotated_frame2 = results2.render()[0]
    cv2.imshow('YOLO Detection', annotated_frame2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        detected_objects = []
        class_names_str = ""
        zoomed_obj = None

        # 모델 2 감지 객체 처리
        for det in results2.xyxy[0]:
            class_id = int(det[5])
            if class_id == 1:  # 예시: 클래스 1만 추적
                x1, y1, x2, y2 = map(int, det[:4])
                detected_obj = frame[y1:y2, x1:x2]
                zoomed_obj = cv2.resize(detected_obj, fixed_size, interpolation=cv2.INTER_LINEAR)

                # 모델 1로 클래스 재추론
                result1 = model1(zoomed_obj)
                for detection in result1.xyxy[0]:
                    x1 = detection[0].item()
                    class_id = int(detection[5].item())
                    class_name = result1.names[class_id]
                    detected_objects.append((1, class_name))

        # 이름 정렬 및 이미지 파일명 구성
        detected_objects.sort(key=lambda obj: obj[0])
        detected_classes = [obj[1] for obj in detected_objects]
        if detected_classes:
            class_names_str = "_".join(detected_classes)
            image_filename = f'{class_names_str}_{time.strftime("%Y%m%d_%H%M%S")}.jpg'
        else:
            img_filename = f'no_detection_{time.strftime("%Y%m%d_%H%M%S")}.jpg'
       
        # 원본 프레임 및 줌된 객체 저장
        cv2.imwrite(img_filename, frame)
        print(f"Frame saved as: {img_filename}")
       
        if zoomed_obj is not None:
            filename_zoom = f"zoomed_object_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename_zoom, zoomed_obj)
            print(f"Zoomed object saved as: {filename_zoom}")

        # S3 경로 고정
        timestamp = datetime.now()
        image_name = f"car_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
        s3_file_key = f"car_images/{image_name}"
       
        # S3 업로드
        _, img_encoded = cv2.imencode('.jpg', original_frame)
        image_data = img_encoded.tobytes()
        s3_url = upload_image_to_s3(s3, image_data, bucket_name, s3_file_key)

        # 데이터베이스 삽입
        if s3_url:
            with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_username,
                ssh_pkey=ssh_private_key_path,
                remote_bind_address=(rds_host, rds_port),
                local_bind_address=('127.0.0.1', 3307)
            ) as tunnel:
                connection = pymysql.connect(
                    host='127.0.0.1',
                    user=rds_username,
                    password=rds_password,
                    database=rds_database,
                    port=tunnel.local_bind_port
                )
                try:
                    with connection.cursor() as cursor:
                        sql = """
                        INSERT INTO TestTable (carpicture, carnum, location, hours, fine)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        data = (
                            s3_url,
                            class_names_str,
                            f'위도:{latitude},경도:{longitude}',
                            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            10000
                        )
                        cursor.execute(sql, data)
                        connection.commit()
                        print("Data inserted successfully into the database.")
                except Exception as e:
                    print("Database insertion error:", e)
                finally:
                    connection.close()

cap.release()
cv2.destroyAllWindows()