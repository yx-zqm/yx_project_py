from dao.detection_dao import DetectionDAO
from service.token_service import TokenService
import xml.etree.ElementTree as ET


class TokenController:
    def __init__(self):
        self.token_service = TokenService()
        self.detection_dao = DetectionDAO()  # 添加 DetectionDAO 实例

    def run(self):
        # 获取用户输入的登录账户
        login_acct = input("Enter login account: ")

        # 创建令牌
        create_response = self.handle_create_token(login_acct)
        print("Create Token Response:")
        print(create_response)

        if create_response:
            # 从创建响应中提取 `APPACCTID` 和 `TOKEN`
            xml_string = create_response['_value_1']
            appacctid, token, create_rsp = self.extract_details(xml_string)

            if create_rsp == '0' and appacctid and token:
                # 检查令牌
                check_response = self.handle_check_token(appacctid, token)
                print("Check Token Response:")
                print(check_response)

                # 打印检查结果
                if check_response:
                    check_xml_string = check_response['_value_1']
                    _, _, check_rsp = self.extract_details(check_xml_string)

                    # 设置检测结果的状态
                    result_status = '成功' if check_rsp == '0' else '失败'

                    # 准备检测数据
                    detection_data = {
                        'task_name': '从帐号短信认证拨测',
                        'task_description': '检测从帐号短信认证流程功能是否正常',
                        'result_status': result_status,
                        'result_details': '请求返回正常',
                        'result_data': '{"response_time": 100, "status_code": 200}',
                        'executor': '4A拨测程序',
                        'configuration': '默认配置',
                        'environment_info': '生产环境',
                        'result_time_range': '100ms',
                        'system_4A': '应用4A'
                    }

                    # 插入检测结果
                    self.detection_dao.insert_detection_result(detection_data)
            else:
                print("Token creation failed or invalid response.")
        else:
            print("No response received from token creation service.")

    def handle_create_token(self, login_acct):
        """处理创建令牌的请求"""
        try:
            response = self.token_service.create_token(login_acct)
            return response
        except Exception as e:
            print(f"Error creating token: {e}")
            return None

    def handle_check_token(self, appacctid, token):
        """处理检查令牌的请求"""
        try:
            response = self.token_service.check_token(appacctid, token)
            return response
        except Exception as e:
            print(f"Error checking token: {e}")
            return None

    def extract_details(self, response_text):
        """解析响应，提取 `APPACCTID`、`TOKEN` 和 `RSP`"""
        try:
            root = ET.fromstring(response_text)
            appacctid = root.findtext('.//APPACCTID')
            token = root.findtext('.//TOKEN')
            rsp = root.findtext('.//RSP')
            return appacctid, token, rsp
        except Exception as e:
            print(f"Error extracting details: {e}")
            return None, None, None