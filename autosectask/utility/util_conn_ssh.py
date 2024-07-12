import paramiko
from autosectask.utility.util_logging import SimpleLogger

logger = SimpleLogger().get_logger()


class SSHConnection:
    def __init__(self, ip, username, password, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.ip, self.port, self.username, self.password)

    def execute_command(self, command):
        logger.info(f"execute shh command [{command}].")
        stdin, stdout, stderr = self.client.exec_command(command)
        terminal = stdout.read().decode()
        if stderr.read().decode():
            logger.error(stderr.read().decode())
        return terminal

    def __enter__(self):
        logger.info("creating shh connection..")
        return self

    def __exit__(self, e_t, e_v, t_b):
        logger.info("releasing ssh connection..")
        self.client.close()


# 示例用法

# 当ssh对象销毁时，连接会自动释放

if __name__ == '__main__':
    ssh = SSHConnection('192.168.198.128', 'fourb', 'Ebupt#202403f')
    output = ssh.execute_command('cd /opt/mcb/smp/program/smc-dataupload-5.1/logs && grep "上报完成" ./du_2024-06*')
    print(output)
