import json
import os

class Config:
    def __init__(self, config_file='config.json'):
        base_dir = os.path.dirname(__file__)
        config_file_path = os.path.abspath(os.path.join(base_dir, config_file))
        print(f"Configuration file path: {config_file_path}")
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Configuration file not found: {config_file_path}")
        with open(config_file_path, 'r') as f:
            self.config = json.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)