import unittest
import time
from service.token_service import TokenService


class TestTokenService(unittest.TestCase):

    def setUp(self):
        """在测试前创建 TokenService 实例"""
        self.service = TokenService()

    def test_create_and_check_token_success(self):
        """测试创建 token 并验证其成功情况"""
        login_acct = 'yx_weixili'

        # Step 1: 创建 token
        create_response = self.service.create_token(login_acct)
        print("Create response:", create_response)

        # 从响应中提取 token 和 appacctid
        token = self.extract_token_from_response(create_response)
        appacctid = self.extract_appacctid_from_response(create_response)
        print(f"Extracted token: {token}")
        print(f"Extracted appacctid: {appacctid}")

        # Step 2: 使用有效 token 进行检查
        check_response = self.service.check_token(appacctid, token)
        print("Check response with valid token:", check_response)

        # 提取 RSP 值
        check_rsp = self.extract_rsp_from_response(check_response)
        print(f"Extracted RSP: {check_rsp}")

        # 验证 token 检查成功
        self.assertEqual(check_rsp, '0', "Token validation should succeed with a valid token.")

    def test_create_and_check_token_invalid(self):
        """测试创建 token 后使用无效 token 验证失败情况"""
        login_acct = 'yx_weixili'

        # Step 1: 创建 token
        create_response = self.service.create_token(login_acct)
        print("Create response:", create_response)
        # 从响应中提取 token 和 appacctid
        token = self.extract_token_from_response(create_response)
        appacctid = self.extract_appacctid_from_response(create_response)
        print(f"Extracted token: {token}")
        # 修改 token 的一部分以模拟无效 token
        invalid_token = self.simulate_invalid_token(token)
        print(f"Simulated invalid token: {invalid_token}")

        # Step 2: 使用无效 token 进行检查
        check_response = self.service.check_token(appacctid, invalid_token)
        print("Check response with invalid token:", check_response)
        # 提取 RSP 值
        check_rsp = self.extract_rsp_from_response(check_response)
        print(f"Extracted RSP: {check_rsp}")
        # 验证 token 检查失败
        self.assertEqual(check_rsp, '1', "Token validation should fail with an invalid token.")

    def test_create_and_check_token_timeout(self):
        """测试 token 超时后的处理"""
        login_acct = 'yx_weixili'
        # Step 1: 创建 token
        create_response = self.service.create_token(login_acct)
        print("Create response:", create_response)
        # 从响应中提取 token 和 appacctid
        token = self.extract_token_from_response(create_response)
        appacctid = self.extract_appacctid_from_response(create_response)
        print(f"Extracted token: {token}")
        print(f"Extracted appacctid: {appacctid}")

        # Step 2: 等待超时时间（例如 3 分钟）
        print("Waiting for 3 minutes to simulate token timeout...")
        time.sleep(10)  # 等待3分钟

        # Step 3: 使用超时后的 token 进行检查
        check_response = self.service.check_token(appacctid, token)
        print("Check response with expired token:", check_response)
        # 提取 RSP 值
        check_rsp = self.extract_rsp_from_response(check_response)
        print(f"Extracted RSP: {check_rsp}")
        # 验证 token 检查失败
        self.assertEqual(check_rsp, '1', "Token validation should fail after timeout.")

    def extract_token_from_response(self, response):
        """从响应中提取 token"""
        response_text = response['_value_1']
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response_text)
        token_node = root.find('.//BODY/TOKEN')
        return token_node.text if token_node is not None else 'N/A'

    def extract_appacctid_from_response(self, response):
        """从响应中提取 APPACCTID"""
        response_text = response['_value_1']
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response_text)
        appacctid_node = root.find('.//BODY/APPACCTID')
        return appacctid_node.text if appacctid_node is not None else 'N/A'

    def extract_rsp_from_response(self, response):
        """从响应中提取 RSP"""
        response_text = response['_value_1']
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response_text)
        rsp_node = root.find('.//BODY/RSP')
        return rsp_node.text if rsp_node is not None else 'N/A'

    def simulate_invalid_token(self, token):
        """模拟无效 token，通过修改 token 的一部分"""
        token_parts = token.split('|')
        if len(token_parts) > 2:
            # 修改 token 的部分内容来模拟无效的 token
            token_parts[16] = '999'  # 修改第17位
            return '|'.join(token_parts)
        return 'invalid_token'


if __name__ == '__main__':
    unittest.main()
