# -*- coding: utf-8 -*-
# @Time    : 2025/8/22 19:37
# @Author  : JasonH
# @File    : PathUtils.py
import os
from pathlib import Path

class PathUtils(object):
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.config_dir = self.root_dir + '\\config\\'
        self.data_resource_dir = self.root_dir + '\\data_resource\\'
        self.log_dir = self.root_dir + '\\Logs\\'
        self.testcases_dir = self.root_dir + '\\testcases\\'
        self.report_dir = self.root_dir + '\\tmp\\allure-report\\'


    def get_api_config_file_path(self):
        """
        获取 api 配置文件名
        :return:
        """
        return self.config_dir + 'cem_config.yaml'

    @staticmethod
    def get_api_config_key(file_path):
        """
        获取 api 配置文件中, api的 key，从而拿到api的地址
        :return:
        """
        file_name = os.path.basename(file_path)
        return Path(file_name).stem.removeprefix('test_') + '_api'


    @staticmethod
    def get_filename(file_path):
        file_name = os.path.basename(file_path)
        return Path(file_name).stem

    @staticmethod
    def get_filename_without_suffix(file_path):
        file_name = os.path.basename(file_path)
        return Path(file_name).stem.removeprefix('test_')

    def get_testcase_data_filename(self, case_file_name):
        """
        通过测试用例的文件名，找到该 测试接口 的测试数据（payload + expect）文件
        :param case_file_name: 测试用例文件名，通过 __file__ 获取
        :return:
        """
        if '.py' in case_file_name:
            # return self.data_resource_dir + case_file_name[0:-3] + '.yaml'
            return self.data_resource_dir + self.get_filename(case_file_name) + '.yaml'
        else:
            return self.data_resource_dir + case_file_name + '.yaml'

# if __name__ == '__main__':
#     p = PathUtils()
#     print(p.root_dir)
#     print(p.data_resource_dir)
#     print(p.log_dir)
#     print(p.report_dir)
#     print(p.config_dir)
#     print()