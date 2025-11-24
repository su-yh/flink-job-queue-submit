# -*- coding: utf-8 -*-
# @Time     : 2025/10/11 17:49
# @Author   : JasonH
# @File     : CemVersion.py


import os
import requests
from utils import YamlData


class CemVersion:
    def __init__(self):
        # 获取当前脚本所在目录的上级目录
        current_dir = os.path.dirname(os.path.dirname(__file__))
        cem_config = YamlData.HandleYaml(current_dir + "\\config\\cem_config.yaml").get_data()
        self.versionApi = cem_config['url'] + cem_config['apis']['server_version_api']
        self.requests_headers = cem_config['request_headers']


    def get_server_version(self):
        payload = 't=1760176078221'
        # 发送请求
        reps = requests.get(self.versionApi, headers=self.requests_headers, params=payload)
        print(reps.json())
        return 'v' + reps.json()['data']['appVersion']

# if __name__ == '__main__':
#     # CemVersion().get_server_version()
#     print(CemVersion().get_server_version())
