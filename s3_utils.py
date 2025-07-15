# s3_utils.py

import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY

def connect_s3():
    return boto3.client(
        service_name="s3",
        region_name="ap-northeast-2",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

def upload_image(s3, bucket, key, image_bytes):
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=image_bytes, ContentType='image/jpeg')
        return f"https://{bucket}.s3.ap-northeast-2.amazonaws.com/{key}"
    except Exception as e:
        print("S3 업로드 실패:", e)
        return None
