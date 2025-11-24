# -*- coding: utf-8 -*-
# @Time    : 2025/8/22 14:48
# @Author  : JasonH
# @File    : Logs.py


import logging
import os
import time


def create_file(log_filename=None):
    """
    创建日志文件（仅支持 None 或绝对路径文件名）
    :param log_filename: 日志文件名（可选）
                        - None：按日期生成日志（项目根目录/Logs/yyyy-mm-dd.log，绝对路径）
                        - 绝对路径字符串：直接使用该绝对路径创建日志文件（需确保路径合法）
    :return: 日志文件完整绝对路径
    """
    # 1. 无参数时：按日期生成（项目根目录/Logs/yyyy-mm-dd.log），转为绝对路径
    if log_filename is None:
        # 项目根目录下的 Logs 文件夹（绝对路径）
        base_log_dir = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), 'Logs'))
        if not os.path.exists(base_log_dir):
            os.makedirs(base_log_dir)  # 支持多级目录创建
        # 按日期生成文件名
        now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        log_file = os.path.abspath(os.path.join(base_log_dir, f"{now_time}.log"))
    # 2. 有参数时：直接使用传入的绝对路径（不做校验，信任用户输入）
    else:
        log_file = log_filename
        # 确保日志文件所在目录存在（即使是绝对路径，也自动创建目录）
        log_file_dir = os.path.dirname(log_file)
        if not os.path.exists(log_file_dir):
            os.makedirs(log_file_dir)

    return log_file


class Log(object):
    def __init__(self, name, log_filename=None, level='DEBUG'):
        self.__name = name
        self.__log_filename = log_filename
        self.__path = create_file(self.__log_filename)
        self.__level = level
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level)

    def __ini_handler(self):
        """初始化handler"""
        self.__logger.handlers.clear()
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.__path, encoding='utf-8')
        return stream_handler, file_handler

    def __set_handler(self, stream_handler, file_handler, level='DEBUG'):
        """设置handler级别并添加到logger收集器"""
        stream_handler.setLevel(level)
        file_handler.setLevel(level)
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    def __set_formatter(self, stream_handler, file_handler):
        """设置日志输出格式"""
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                      '-%(levelname)s-[日志信息]: %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    def __close_handler(self, stream_handler, file_handler):
        """关闭handler"""
        stream_handler.close()
        file_handler.close()

    @property
    def Logger(self):
        """构造收集器，返回looger"""
        stream_handler, file_handler = self.__ini_handler()
        self.__set_handler(stream_handler, file_handler)
        self.__set_formatter(stream_handler, file_handler)
        self.__close_handler(stream_handler, file_handler)
        return self.__logger


