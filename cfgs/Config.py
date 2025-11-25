
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum, unique

from utils.YamlData import HandleYaml


class Config:

    def __init__(self, file_path: str, prev = "base"):
        self.file_path = file_path
        data = HandleYaml.get_data(file_path)
        self.data = data[prev]
        self.properties: BaseProperties = BaseProperties(**self.data)

    def get_data(self):
        return self.properties


@unique
class JobNameEnum(str, Enum):
    """jobName 枚举类：限定只能取以下三个值"""
    COHORT = "cohort"       # 队列相关作业
    REALTIME = "realtime"   # 实时相关作业
    REPETITION = "repetition"  # 重复相关作业

    # 可选：自定义枚举的描述（便于日志/文档）
    @property
    def description(self):
        desc_map = {
            self.COHORT: "队列相关作业",
            self.REALTIME: "实时相关作业",
            self.REPETITION: "重复相关作业"
        }
        return desc_map[self]


class FlinkProperties(BaseModel):
    enable: bool = Field(..., description="启用/禁用")
    job_name: JobNameEnum = Field(..., description=f"作业名称")


class BaseProperties(BaseModel):
    logger_file_path: str = Field(..., description="日志文件路径")
    base_url: str = Field(..., description="http://localhost:8991")
    flink_home: str = Field(..., description="flink 家目录")
    date_start: int = Field(..., description="开始日期")
    days: int = Field(..., description="天数")
    flink: list[FlinkProperties] = Field(..., description="flink 相关的配置")
    pns: Optional[list[str]] = Field(None, description="pns")
    channels: Optional[list[str]] = Field(None, description="channels")

    def get_pns(self) -> str:
        """将 pns 列表转为逗号分隔字符串，自动处理 None 和空值"""
        if self.pns is None:
            return ""
        valid_pns = [item.strip() for item in self.pns if item and item.strip()]
        return ",".join(valid_pns)

    def get_channels(self) -> str:
        if self.channels is None:
            return ""
        valid_pns = [item.strip() for item in self.channels if item and item.strip()]
        return ",".join(valid_pns)






# # 3. 使用示例（验证枚举的校验效果）
# if __name__ == "__main__":
#     cfg = Config("../config.yaml")
#     properties: BaseProperties = cfg.get_data()
#     print(f"cfg.flink: {properties.flink}")










