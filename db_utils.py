# db_utils.py

from sshtunnel import SSHTunnelForwarder
import pymysql
from config import *

def save_to_db(s3_url, class_str, lat, lon, timestamp):
    with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_pkey=SSH_KEY_PATH,
        remote_bind_address=(RDS_HOST, RDS_PORT),
        local_bind_address=('127.0.0.1', 3307)
    ) as tunnel:
        conn = pymysql.connect(
            host='127.0.0.1',
            user=RDS_USER,
            password=RDS_PW,
            database=RDS_DB,
            port=tunnel.local_bind_port
        )
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO TestTable (carpicture, carnum, location, hours, fine)
                    VALUES (%s, %s, %s, %s, %s)
                """
                location = f"위도:{lat},경도:{lon}"
                cursor.execute(sql, (s3_url, class_str, location, timestamp, 10000))
                conn.commit()
                print("DB 저장 완료")
        except Exception as e:
            print("DB 저장 실패:", e)
        finally:
            conn.close()
