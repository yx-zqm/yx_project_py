import zeep
from datetime import datetime
import logging
from config.config import Config

logging.basicConfig(level=logging.INFO)

class CreateSoapClient:
    def __init__(self):
        self.config = Config()
        self.wsdl_url = self.config.get('create_wsdl_url')
        self.client = zeep.Client(self.wsdl_url)

    def create_token(self, login_acct):
        timestamp = datetime.now().strftime(self.config.get('timestamp_format'))
        request = f"""<?xml version="1.0" encoding="UTF-8"?>
        <USERREQ>
            <HEAD>
                <CODE>000</CODE>
                <SID>000</SID>
                <TIMESTAMP>{timestamp}</TIMESTAMP>
                <SERVICEID>{self.config.get('service_id')}</SERVICEID>
            </HEAD>
            <BODY>
                <LOGINACCT>{login_acct}</LOGINACCT>
            </BODY>
        </USERREQ>"""
        try:
            response = self.client.service.CreateAiuapTokenSoap(RequestInfo=request)
            if response and '<ERROR_CODE>' in response:
                logging.error("Error in response: %s", response)
                return None
            return response
        except Exception as e:
            logging.error(f"Error during create_token: {e}")
            return None

class CheckSoapClient:
    def __init__(self):
        self.config = Config()
        self.wsdl_url = self.config.get('check_wsdl_url')
        self.client = zeep.Client(self.wsdl_url)

    def check_token(self, appacctid, token):
        timestamp = datetime.now().strftime(self.config.get('timestamp_format'))
        request = f"""<?xml version="1.0" encoding="UTF-8"?>
        <USERREQ>
            <HEAD>
                <CODE></CODE>
                <SID></SID>
                <TIMESTAMP>{timestamp}</TIMESTAMP>
                <SERVICEID>{self.config.get('service_id')}</SERVICEID>
                <CHANNEL></CHANNEL>
            </HEAD>
            <BODY>
                <APPACCTID>{appacctid}</APPACCTID>
                <TOKEN>{token}</TOKEN>
            </BODY>
        </USERREQ>"""
        try:
            response = self.client.service.CheckAiuapTokenSoap(RequestInfo=request)
            if response and '<ERROR_CODE>' in response:
                logging.error("Error in response: %s", response)
                return None
            return response
        except Exception as e:
            logging.error(f"Error during check_token: {e}")
            return None