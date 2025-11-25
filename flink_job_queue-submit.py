import requests
import os
import sys
import time
from utils.Logs import Log
from utils import YamlData

cfg = YamlData.HandleYaml("config.yaml")

file = os.path.basename(sys.argv[0])
log = Log(file, cfg.get_value("base.logger.file-path"))
logger = log.Logger

base_url = "http://192.168.8.143:8991"
# base_url = "http://localhost:8991"

def get_jobs_overview():
    try:
        url = base_url + "/jobs/overview"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
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
                            print(f"集群中的作业，ID: {job.get('jid')}，名称：{job.get('name')}，状态：{job_status}")
                        # case "FAILED" | "CANCELED" | "FINISHED":
                        # case _:

                if flink_cluster_idle:
                    print("Flink cluster is idle")
                    return True
            else:
                print("返回的数据中未包含 'jobs' 字段，无法解析作业信息。")
                return False
    pass



if __name__ == "__main__":
    flink_cluster_idle = wait_flink_cluster_idle(3600)
    logger.info(f"flink_cluster_idle: {flink_cluster_idle}")
    if not flink_cluster_idle:
        sys.exit(1)

    exit_code = os.system("cd /home/suyunhong/flink/flink-merge/flink-1.18.0 && ./bin/stop-cluster.sh")
    if exit_code != 0:
        print(f"exit_code: {exit_code}")
        sys.exit(1)

    flink_cluster_idle = wait_flink_cluster_idle(30)
    if not flink_cluster_idle:
        print(f"未启动成功。")
        sys.exit(1)

    # 启动成功，10 秒后开始提交作业
    for i in range(10):
        time.sleep(1)




