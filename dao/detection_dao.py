import mysql.connector
from mysql.connector import Error
from config.config import Config
from datetime import datetime


class DetectionDAO:
    def __init__(self):
        self.config = Config()
        self.host = self.config.get('db_host')
        self.user = self.config.get('db_user')
        self.password = self.config.get('db_password')
        self.database = self.config.get('db_name')
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Database connection established.")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def insert_detection_result(self, detection_data):
        """插入检测结果到数据库"""
        if self.connection is None or not self.connection.is_connected():
            self.connect()

        cursor = self.connection.cursor()

        # 获取当前时间并格式化
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        insert_query = """
            INSERT INTO detection_results (
                detection_timestamp, task_name, task_description, 
                target_url, result_status, result_details, result_data, 
                executor, configuration, environment_info, result_time_range, 
                detection_type, system_4A
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        values = (
            current_time,  # 使用当前时间作为 detection_timestamp
            detection_data.get('task_name'),
            detection_data.get('task_description'),
            self.config.get('check_wsdl_url'),  # 将 target_url 设置为 check_wsdl_url 的值
            detection_data.get('result_status'),
            detection_data.get('result_details'),
            detection_data.get('result_data'),
            detection_data.get('executor'),
            detection_data.get('configuration'),
            detection_data.get('environment_info'),
            detection_data.get('result_time_range'),
            '账号拨测',  # 将 detection_type 设置为 '账号拨测'
            detection_data.get('system_4A')
        )

        try:
            cursor.execute(insert_query, values)
            self.connection.commit()
            print("Detection result inserted successfully.")
        except Error as e:
            print(f"Error inserting detection result: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")