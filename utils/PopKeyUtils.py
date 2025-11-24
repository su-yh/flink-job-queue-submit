# -*- coding: utf-8 -*-
# @Time     : 2025/9/28 17:59
# @Author   : JasonH
# @File     : PopKeyUtils.py

class PopKeyUtils(object):
    def __init__(self, reps_json):
        self.reps_json = reps_json

    '''
    响应body的json.data.list[0]中带有一个随机的uuid，需要剔除后再断言
    在此提供一个剔除json key的函数
    
    主要适用于 列表接口的response校验
    比如：
    {
      "code" : 0,
      "message" : "SUCCESS",
      "data" : {
        "list" : [ {
          "id" : "4346605",
          "code" : "code_418",
          "pnum" : "phone_202350687",
          "payType" : "1",
          "uuid" : "df2488977ec84367bd155b72a9fa4162"
        } ],
        "total" : "1"
      }
    }
    '''
    def pop_key_in_dataList(self, key=None):
        if key is None:
            key = 'uuid'
        for item in self.reps_json['data']['list']:
            item.pop(key, None)
        return self.reps_json

    '''
    响应body的json.data.list[0]和data.list[0].financialAccountList[0]中中带有一个随机的uuid，需要剔除后再断言
    在此提供一个剔除json key的函数

    主要适用于 列表接口（Agent Information页面的列表查询）的response校验
    比如：
    {
      "code" : 0,
      "message" : "SUCCESS",
      "data" : {
        "list" : [ {
          "id" : "182",
          "code" : "testcode_2",
          "level" : 1,
          "pnum" : "test_agent_phone_2",
          "remittanceLimited" : "NORMAL",
          "creditAmount" : 0.00,
          "remittanceAddress" : "suyh_address7",
          "svipAuditStatus" : "NON_SUBMIT",
          "svipSystemOnline" : "OFFLINE",
          "balance" : 0.00,
          "svipVipType" : "PROXY",
          "financialAccountList" : [ {
            "id" : "1711",
            "financialCategory" : "UPI",
            "financialAccount" : "atpp_4b0529860fed41ea9b6a974c4a75003c",
            "uuid" : "8dd8cebd30384025a7c5ceab78ff5960"
          } ],
          "uuid" : "b6a4ea0532f948e6b86051bb6dc093a5",
          "schedulingEnabled" : "DISABLE",
          "transferBalance" : 0.00,
          "transferCount" : 0
        }],
        "total" : "3"
      }
    }
    '''

    def pop_key_in_dataListAndDataKeyList(self, data_key_list=None, key=None):
        if key is None:
            key = 'uuid'
        if data_key_list is None:
            data_key_list = 'financialAccountList'
        for item in self.reps_json['data']['list']:
            for data_key_item in item[data_key_list]:
                data_key_item.pop(key, None)
            item.pop(key, None)
        return self.reps_json

    '''
    响应body的json.data.list[0]中带有created和updated，需要剔除后再断言
    在此提供一个剔除json key的函数

    主要适用于 列表接口(机器人白名单列表)的response校验
    比如：
    {
      "code" : 0,
      "message" : "SUCCESS",
      "data" : {
        "list" : [ {
          "id" : "9",
          "chatId" : "-1003114550924",
          "remark" : "cem-autotest群",
          "enable" : "ENABLE",
          "created" : "2025-10-11 14:57:06",
          "updated" : "2025-10-11 14:57:06"
        } ],
        "total" : "1"
      }
    }
    '''

    def pop_keys_in_dataList(self, keys=None):
        if keys is None:
            keys = ['created', 'updated']
        for key in keys:
            for item in self.reps_json['data']['list']:
                item.pop(key, None)
        return self.reps_json

    '''
    响应body的json中包含几个时间戳字段，需要剔除后再断言
    主要适用于 业务校验不通过时的response校验
    比如：
    {
    "timestamp": "2025-09-30 07:28:27",
    "status": 200,
    "path": "/prod-api/abnormal/transfer/update/pn",
    "timestamp_zh": "2025-09-30 09:58:27.107",
    "code": 1026007,
    "message": "Merchant No has been edited and cannot be edited again."
    }
    '''
    def pop_keys_in_json(self, key_list=None):
        if key_list is None:
            key_list = ['timestamp', 'timestamp_zh']
        for key in key_list:
            if key in self.reps_json:
                self.reps_json.pop(key, None)
        return self.reps_json

    '''
    响应body的json.data中带有一个随机的uuid，需要剔除后再断言
    在此提供一个剔除json key的函数

    主要适用于 详情接口的response校验
    比如：
    {
      "code" : 0,
      "message" : "SUCCESS",
      "data" : {
        "id" : "8908",
        "dates" : 20250826,
        "refundNo" : "refund2025082696814d6d15ce",
        "code" : "CODE6383",
        "refundFromUpi" : "sgara@example.com",
        "refundToUpi" : "warinder05@example.com",
        "utr" : "UTR177890484060",
        "amount" : 4646.58,
        "pn" : "USD",
        "paymentUid" : "UID56344",
        "status" : "WAITING",
        "upiCardNo" : "180038494592480",
        "ifsc" : "IFSC7012",
        "mtime" : "2025-08-31 07:29:54",
        "transactionTime" : "2025-08-26 06:04:54",
        "imgUploadTime" : "2025-08-26 15:04:54",
        "created" : "2025-08-26 15:04:54",
        "updated" : "2025-08-27 09:04:54",
        "url" : [ "https://picsum.photos/800/600?id=dbac423c", "https://picsum.photos/800/600?id=be2c0aaf", "https://dummyimage.com/800x600?id=42cd2e14", "https://picsum.photos/800/600?id=8eace241" ],
        "uuid" : "0b00c083a8874ff28b6bf83bc68d3c8f"
      }
    }
    '''

    def pop_key_in_data(self, key=None):
        if key is None:
            key = 'uuid'
        if key in self.reps_json['data']:
            self.reps_json['data'].pop(key, None)
        return self.reps_json
