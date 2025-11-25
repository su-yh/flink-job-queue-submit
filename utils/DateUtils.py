from datetime import datetime, timezone, timedelta
from typing import Optional, Union



class DateUtils:

    @staticmethod
    # 计算得到日期对应偏移量的日期
    def calculate_target_date(dates: int, n: int) -> Optional[int]:
        """
        计算整数格式日期的目标日期：n>0算未来，n<0算历史，n=0算当天

        :param dates: 原始日期（整数格式，如20240121）
        :param n: 日期偏移天数（正数=未来，负数=历史，0=当天）
        :return: 目标日期（整数格式），失败时返回None
        """
        # 整数日期转字符串（确保8位格式，避免如202421这类非法输入）
        date_str = str(dates)
        original_date = datetime.strptime(date_str, "%Y%m%d")

        # 计算目标日期：直接用n作为timedelta的天数（天然适配正/负/0）
        target_date = original_date + timedelta(days=n)

        # 目标日期转回整数格式（保持与原始日期一致的8位整数）
        target_date_int = int(target_date.strftime("%Y%m%d"))

        return target_date_int



