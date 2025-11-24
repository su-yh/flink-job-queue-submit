# -*- coding: utf-8 -*-
# @Time    : 2025/8/22 14:43
# @Author  : JasonH
# @File    : Assert.py



"""
封装Assert方法

"""
from utils.Logs import Log
from utils import Consts
import json


class Assertions:
    def __init__(self, def_name):
        # self.log = Log.MyLog()
        self.def_name = def_name
        log = Log(def_name)
        self.logger = log.Logger

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert code == expected_code
            self.logger.info("statusCode true, expected_code is %s, statusCode is %s " % (expected_code, code))
            # return True
        except:
            self.logger.error("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))
            Consts.RESULT_LIST.append('fail')
            raise

    def assert_value_by_key(self, body, body_key, expected_value):
        """
        验证response body中任意属性的值
        :param body:
        :param body_key:
        :param expected_value:
        :return:
        """
        try:
            msg = body[body_key]
            assert msg == expected_value
            self.logger.info(
                "Response body value == expected_value, expected_value is %s, body_value is %s" % (expected_value, body[body_key]))
            # return True

        except:
            self.logger.error(
                "Response body value != expected_value, expected_value is %s, body_value is %s" % (expected_value, body[body_key]))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_value_in_body(self, body, expected_value):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_value:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_value in text
            self.logger.info("Response body contain expected_value, expected_value is %s" % expected_value)
            # return True

        except:
            self.logger.error("Response body Does not contain expected_value, expected_value is %s" % expected_value)
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_body_equal(self, body, expected_body):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_body:
        :return:
        """
        try:
            assert body == expected_body
            self.logger.info("Response body = expected_body, expected_body is %s, body is %s" % (expected_body, body))
            # return True

        except:
            self.logger.error("Response body != expected_body, expected_body is %s, body is %s" % (expected_body, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_time(self, req_time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param req_time:
        :param expected_time:
        :return:
        """
        try:
            assert req_time < expected_time
            self.logger.info(
                "Response time < expected_time, expected_time is %s, time is %s" % (expected_time, req_time))
            # return True

        except:
            self.logger.error("Response time > expected_time, expected_time is %s, time is %s" % (expected_time, req_time))
            Consts.RESULT_LIST.append('fail')
            raise
