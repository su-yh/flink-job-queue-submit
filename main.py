import requests
import os
import sys
import time
from utils.Logs import Log
from utils.DateUtils import DateUtils
from utils import YamlData
from cfgs.Config import Config, BaseProperties, FlinkProperties, JobNameEnum

# cfg = YamlData.HandleYaml("config.yaml")
cfg: Config = Config("config.yaml")
properties: BaseProperties = cfg.properties

file = os.path.basename(sys.argv[0])
log = Log(file, properties.logger_file_path)
logger = log.Logger

# base_url = "http://192.168.8.143:8991"
# base_url = "http://localhost:8991"
base_url = properties.base_url

def get_jobs_overview():
    url = base_url + "/jobs/overview"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.info(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.info(f"请求（{url}）发生异常: {e}")
        return None


def wait_flink_cluster_idle(seconds: int):
    s: int = 0
    while True:
        if s >= seconds:
            break
        s += 1

        time.sleep(1)

        jobs_info = get_jobs_overview()
        if jobs_info:
            if 'jobs' in jobs_info:
                flink_cluster_idle = True
                for job in jobs_info['jobs']:
                    # INITIALIZING, CREATED, RUNNING, FAILING, CANCELLING, RESTARTING, SUSPENDED, RECONCILING
                    # FAILED, CANCELED, FINISHED
                    job_status = job.get('state')
                    match job_status:
                        case "INITIALIZING" | "CREATED" | "RUNNING" | "FAILING" | "CANCELLING" | "RESTARTING" | "SUSPENDED" | "RECONCILING":
                            flink_cluster_idle = False
                            logger.info(f"集群中的作业，ID: {job.get('jid')}，名称：{job.get('name')}，状态：{job_status}")
                        # case "FAILED" | "CANCELED" | "FINISHED":
                        # case _:

                if flink_cluster_idle:
                    logger.info("Flink cluster is idle")
                    return True
            else:
                logger.info("返回的数据中未包含 'jobs' 字段，无法解析作业信息。")
                return False
    pass


def job_start(f: FlinkProperties, dates: int):
    match f.job_name:
        case JobNameEnum.COHORT:
            cohort_start(f, dates)

        case JobNameEnum.REALTIME:
            realtime_start(f, dates)

        case JobNameEnum.REPETITION:
            repetition_start(f, dates)

        case _:
            raise ValueError(f"不支持的作业类型：{f.job_name.value}")


def cohort_start(f: FlinkProperties, dates: int):
    if not f.enable:
        return

    os.system(f"cd /home/suyunhong/flink/flink-merge/flink-1.18.0 && "
              f"./bin/flink run -Dexecution.runtime-mode=BATCH -d job-jar/flink-cohort-job-*.jar --cds.flink.batch.date=${dates} "
              f"--cds.flink.batch.pns={f.get_pns()} --cds.flink.batch.channel-list={f.get_channels()}")
    logger.info(f"启动同期群作业, dates: {dates}")

def realtime_start(f: FlinkProperties, dates: int):
    if not f.enable:
        return

    logger.info(f"实时曲线作业, dates: {dates}")
    pass

def repetition_start(f: FlinkProperties, dates: int):
    if not f.enable:
        return
    logger.info(f"重复率作业, dates: {dates}")
    pass


if __name__ == "__main__":

    flink_cluster_idle = wait_flink_cluster_idle(3600)
    logger.info(f"flink_cluster_idle: {flink_cluster_idle}")
    if not flink_cluster_idle:
        sys.exit(1)

    exit_code = os.system("cd /home/suyunhong/flink/flink-merge/flink-1.18.0 && ./restart.sh")
    if exit_code != 0:
        logger.info(f"exit_code: {exit_code}")
        sys.exit(1)

    flink_cluster_idle = wait_flink_cluster_idle(30)
    if not flink_cluster_idle:
        logger.info(f"未启动成功。")
        sys.exit(1)

    # 启动成功，10 秒后开始提交作业
    for i in range(10):
        time.sleep(1)


    for i in range(properties.days):
        dates = DateUtils.calculate_target_date(properties.date_start, i)

        logger.info(f"dates: {dates}")
        for f in properties.flink:
            job_start(f, dates)

            flag = wait_flink_cluster_idle(86400)
            if not flag:
                break


