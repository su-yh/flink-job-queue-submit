# -*- coding: utf-8 -*-
# @Time     : 2025/9/20 20:43
# @Author   : JasonH
# @File     : MysqlUtils.py
import os

import pymysql
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

"""
MysqlUtils.py
"""
class MysqlUtils(object):
    def __init__(self):
        cem_port = os.getenv('CEM_MYSQL_PORT')
        payout_port = os.getenv('PAYOUT_MYSQL_PORT')

        if not cem_port or not cem_port.isdigit():
            raise ValueError("CEM_MYSQL_PORT is missing or invalid")
        if not payout_port or not payout_port.isdigit():
            raise ValueError("PAYOUT_MYSQL_PORT is missing or invalid")

        self.cem_mysql_config = {
            'host': os.getenv('CEM_MYSQL_HOST'),
            'port': int(cem_port),
            'user': os.getenv('CEM_MYSQL_USER'),
            'password': os.getenv('CEM_MYSQL_PASSWORD'),
            'db': os.getenv('CEM_MYSQL_DATABASE'),
            'charset': os.getenv('CEM_MYSQL_CHARSET')
         }
        self.payout_mysql_config = {
            'host': os.getenv('PAYOUT_MYSQL_HOST'),
            'port': int(payout_port),
            'user': os.getenv('PAYOUT_MYSQL_USER'),
            'password': os.getenv('PAYOUT_MYSQL_PASSWORD'),
            'db': os.getenv('CEM_MYSQL_DATABASE'),
            'charset': os.getenv('PAYOUT_MYSQL_CHARSET')
        }
        # 验证数据库配置
        for config, module in [(self.cem_mysql_config, 'cem'), (self.payout_mysql_config, 'payout')]:
            if not config['db']:
                raise ValueError(f"{module.upper()}_MYSQL_DB is not set or empty")

    def get_cem_mysql_conn(self):
        cem_mysql_conn = pymysql.connect(**self.cem_mysql_config)
        return cem_mysql_conn

    def get_payout_mysql_conn(self):
        payout_mysql_conn = pymysql.connect(**self.payout_mysql_config)
        return payout_mysql_conn

    def mysql_query(self, module, sql, params=None):
        conn = self.get_payout_mysql_conn() if module == 'payout' else self.get_cem_mysql_conn()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def mysql_update(self, module, sql, params=None):
        conn = self.get_payout_mysql_conn() if module == 'payout' else self.get_cem_mysql_conn()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()

    def mysql_insert(self, module, sql):
        conn = self.get_payout_mysql_conn() if module == 'payout' else self.get_cem_mysql_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            return cursor.lastrowid

    def mysql_delete(self, module, sql, params=None):
        conn = self.get_payout_mysql_conn() if module == 'payout' else self.get_cem_mysql_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)  # 支持参数化查询
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def mysql_truncate(self, module, table_name):
        '''
        高危动作，清谨慎操作！！！
        :param module:
        :param table_name:
        :return:
        '''
        conn = self.get_payout_mysql_conn() if module == 'payout' else self.get_cem_mysql_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(f'TRUNCATE TABLE {table_name}')
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()




