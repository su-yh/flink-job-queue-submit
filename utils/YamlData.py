# -*- coding: utf-8 -*-
# @Time    : 2025/8/22 15:17
# @Author  : JasonH
# @File    : YamlData.py


import os
import yaml
from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.scanner import ScannerError

from utils.PathUtils import PathUtils


# 初始化ruamel.yaml的RoundRipLoader和RoundTripDumper
# ryaml = YAML(typ='rt')

class HandleYaml:

    def __init__(self, file_path=None):
        """
            初始化函数
            :param file_path: 文件路径，可选参数，默认为None
        """
        if file_path:
            self.file_path = file_path
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))
            # os.path.abspath('.')表示获取当前文件所在目录；os.path.dirname表示获取文件所在父目录；所以整个就是项目的所在路径
            print(root_dir)
            self.file_path = root_dir + '\\config\\cem-config.yaml'  # 获取文件所在的相对路径(相对整个项目)
            # self.data = self.get_data()

    # def get_data_fullLoad(self):
    #     fp = open(self.file_path, encoding='utf-8')
    #     data = yaml.load(fp, Loader=yaml.FullLoader)
    #     yaml.warnings({'YAMLLoadWarning': False})
    #     return data


    def get_data(self):
        """
            从指定路径读取YAML格式文件并返回解析后的数据
            Returns:
                dict/list: YAML文件解析后的数据结构
            Raises:
                FileNotFoundError: 当指定文件不存在时
                PermissionError: 当没有权限读取文件时
                ValueError: 当YAML文件格式错误时
                RuntimeError: 当发生其他未知错误时
        """
        try:
            with open(self.file_path, "r", encoding='utf-8') as fp:
                data = YAML(typ='rt').load(fp)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"文件 {self.file_path} 不存在")
        except PermissionError:
            raise PermissionError(f"没有权限读取文件 {self.file_path}")
        except ScannerError as e:
            print(f"解析 YAML 文件时出错: {e}")
            print(f"问题出现在行 {e.context_mark.line + 1}, 列 {e.context_mark.column + 1}")
            print(f"详细信息: {e.problem}")
            with open('file.yaml', 'r', encoding='utf-8') as fp:
                lines = fp.readlines()
                print("文件内容：")
                for i, line in enumerate(lines, 1):
                    print(f"Line {i}: {line.strip()}")
        except YAMLError as e:
            raise ValueError(f"YAML文件格式错误: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"读取文件时发生未知错误: {str(e)}")


    def get_data_by_key(self, key):
        """
            根据指定键获取数据
            参数:
                key: 要查找的键值
            返回:
                与指定键关联的数据值
            异常:
                KeyError: 当键不存在或数据类型不支持键访问时抛出
        """
        data = self.get_data()
        try:
            return data[key]
        except (KeyError, TypeError) as e:
            raise KeyError(f"Key '{key}' not found in data") from e


    def update_data(self, key, value):
        """
            更新数据文件中的指定键值对
            参数:
                key: 要更新的键
                value: 要设置的新值
            返回值:
                无返回值
            异常:
                Exception: 当数据更新失败时抛出异常
        """
        try:
            data = self.get_data()
            data[key] = value
            with open(self.file_path, 'w', encoding='utf-8') as fp:
                YAML(typ='rt').dump(data, fp)
        except Exception as e:
            # 可以根据实际需求添加日志记录或重新抛出异常
            raise Exception(f"Failed to update data: {str(e)}")


    @staticmethod
    def get_api_test_url(file_path):

        # 获取api配置文件，即 /config/cem_config.yaml 文件
        api_config_file = PathUtils().get_api_config_file_path()
        api_config_data = HandleYaml(api_config_file).get_data()
        # print(api_config_file)

        # 获取api在配置文件中的 key，从而获取api的地址
        api_name = PathUtils().get_api_config_key(file_path)

        api_url = api_config_data['url'] + api_config_data['apis'][api_name]
        requests_headers = api_config_data['request_headers']

        # 返回api的url 和 headers
        return api_url, requests_headers

    @staticmethod
    def get_api_test_data(file_path, def_name):

        # 获取api的测试数据文件，即 /data_resource/test_xxxxx.yaml 文件
        api_config_file = PathUtils().get_testcase_data_filename(file_path)
        api_config_data = HandleYaml(api_config_file).get_data()

        # 获取api的测试数据，并返回 payload 和 expect
        payload = api_config_data[def_name]['payload']
        expect = api_config_data[def_name]['expect']
        # 返回一个元组： payload, expect
        return payload, expect

# if __name__ == '__main__':
#     yaml_data = HandleYaml()
#     print(yaml_data.get_data())
