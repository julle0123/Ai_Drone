# config.py

S3_BUCKET = "capstone2024s3"

# AWS Credentials
AWS_ACCESS_KEY = "AKIA********"
AWS_SECRET_KEY = "**********************"

# SSH
SSH_HOST = '43.203.251.33'
SSH_PORT = 22
SSH_USER = 'ubuntu'
SSH_KEY_PATH = '/home/jetson/capstoneKEY.pem'

# RDS
RDS_HOST = 'capstone2024.cjygcowwu2k3.ap-northeast-2.rds.amazonaws.com'
RDS_PORT = 3306
RDS_USER = 'admin'
RDS_PW = 'capstone2024'
RDS_DB = 'capstone2024'

# 모델 경로
MODEL_CAR_PATH = "/home/jetson/yolov5/best.pt"
MODEL_PLATE_PATH = "/home/jetson/yolov5/num.pt"
