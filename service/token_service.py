from dao.detection_dao import DetectionDAO
from dao.soap_clients import CreateSoapClient, CheckSoapClient

class TokenService:
    def __init__(self):
        self.create_client = CreateSoapClient()
        self.check_client = CheckSoapClient()
        self.detection_dao = DetectionDAO()  # 不传递额外参数

    def create_token(self, login_acct):
        try:
            response = self.create_client.create_token(login_acct)
            return response
        except Exception as e:
            print(f"Error creating token: {e}")
            return None

    def check_token(self, appacctid, token):
        try:
            response = self.check_client.check_token(appacctid, token)
            return response
        except Exception as e:
            print(f"Error checking token: {e}")
            return None