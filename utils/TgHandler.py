# -*- coding: utf-8 -*-
# @Time     : 2025/8/28 10:52
# @Author   : JasonH
# @File     : TgHandler.py

import json
import os
import time

import requests
from dotenv import load_dotenv
from utils.PathUtils import PathUtils
from utils.CemVersion import CemVersion

# 加载环境变量
load_dotenv()

# Telegram 配置
# BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

class TgHandler(object):
    def __init__(self, allure_result_dir=None, allure_report_dir=None):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not self.bot_token or not self.chat_id:
            raise "Telegram Bot Token 或 Chat ID 未配置"

        self.telegram_msg_api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        if allure_result_dir:
            self.allure_result_dir = allure_result_dir
        else:
            self.allure_result_dir = PathUtils().root_dir + './tmp/allure-results'

        self.telegram_doc_api_url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
        if allure_report_dir:
            self.allure_report_dir = allure_report_dir
        else:
            self.allure_report_dir = PathUtils().root_dir + './tmp/allure-report'


    def parse_allure_results(self):
        """解析 Allure 结果目录中的 JSON 文件"""
        passed = 0
        failed = 0
        skipped = 0
        broken = 0
        failed_cases = []

        allure_result_dir = self.allure_result_dir
        if not os.path.exists(allure_result_dir):
            return None, "Allure 结果目录不存在"

        for file_name in os.listdir(allure_result_dir):
            if file_name.endswith('.json'):
                try:
                    with open(os.path.join(allure_result_dir, file_name), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        status = data.get('status')
                        if status == 'passed':
                            passed += 1
                        elif status == 'failed':
                            failed += 1
                            failed_cases.append(data.get('name', 'Unknown'))
                        elif status == 'skipped':
                            skipped += 1
                        elif status == 'broken':
                            broken += 1
                            failed_cases.append(data.get('name', 'Unknown'))
                except Exception as e:
                    return None, f"解析 Allure 文件 {file_name} 失败: {str(e)}"

        total = passed + failed + skipped + broken
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'broken': broken,
            'failed_cases': failed_cases,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'fail_rate': (failed / total * 100) if total > 0 else 0,
            'skip_rate': (skipped / total * 100) if total > 0 else 0,
            'broken_rate': (broken / total * 100) if total > 0 else 0
        }, None

    def send_telegram_message(self, tg_message, parse_mode='Markdown'):
        """发送消息到 Telegram"""
        if not self.bot_token or not self.chat_id:
            return False, "Telegram Bot Token 或 Chat ID 未配置"

        payload = {
            'chat_id': self.chat_id,
            'text': tg_message,
            'parse_mode': parse_mode
        }
        try:
            response = requests.post(self.telegram_msg_api_url, json=payload, timeout=10)
            if response.status_code == 200:
                return True, "消息发送成功"
            else:
                return False, f"消息发送失败: {response.text}"
        except Exception as e:
            raise f"消息发送失败: {str(e)}"

    def send_results_to_telegram(self):
        """主函数：解析 Allure 结果并发送到 Telegram"""
        results, error = self.parse_allure_results()
        if error:
            return False, error

        # 格式化时间
        current_time = time.strftime('%Y-%m-%d %H:%M', time.localtime())

        # 获取项目版本
        project_version = CemVersion().get_server_version()

        project_name = os.getenv('PROJECT_NAME', '未命名项目')
        tg_message = f"""
        📊 *自动化测试报告* 📅 {current_time}
        🔹 *项目*: {project_name} (版本: {project_version})
        🔹 *总用例数*: {results['total']}
        ✅ *通过用例数及其占比*: {results['passed']} ({results['pass_rate']:.2f}%)
        ❌ *失败用例数及其占比*: {results['failed']} ({results['fail_rate']:.2f}%)
        ⏭ 跳过用例数及其占比: {results['skipped']} ({results['skip_rate']:.2f}%)
        ⚠ *异常用例数及其占比*: {results['broken']} ({results['broken_rate']:.2f}%)
        """

        if results['failed_cases']:
            # tg_message += "\n*失败用例*:\n" + "\n".join([f"- {case}" for case in results['failed_cases']])
            # 限制显示最多 5 个失败用例，避免消息过长
            failed_cases = results['failed_cases'][:5]
            tg_message += "*失败用例*: \n" + "\n".join([f"  • {case}" for case in failed_cases])
            if len(results['failed_cases']) > 5:
                tg_message += f"\n  • ...还有 {len(results['failed_cases']) - 5} 个失败用例"

        send_result, msg = self.send_telegram_message(tg_message)
        return send_result, msg


    def send_report_doc_to_telegram(self):
        """发送 Allure 报告文件到 Telegram"""
        """Allure 报告文件 index 文件中 未集成测试结果，发到tg上看不到测试结果，先停用！！！"""
        report_file = os.path.join(self.allure_report_dir, 'index.html')
        if not os.path.exists(report_file):
            print("报告文件不存在")
            return

        with open(report_file, 'rb') as f:
            payload = {
                'chat_id': self.chat_id,
                'caption': 'Allure 测试报告'
            }
            files = {'document': f}
            response = requests.post(self.telegram_doc_api_url, data=payload, files=files)
            if response.status_code == 200:
                print("报告文件发送成功")
                return True, "报告文件发送成功"
            else:
                print(f"报告文件发送失败: {response.text}")
                raise "报告文件发送失败"


# if __name__ == '__main__':
#     # allure_results_dir = PathUtils().root_dir + './tmp/allure-results'
#     success, message = TgHandler().send_results_to_telegram()
#     TgHandler().send_report_doc_to_telegram()
#     print(message)