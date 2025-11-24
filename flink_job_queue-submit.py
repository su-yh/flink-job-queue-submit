import requests
import os
import sys
import time
from utils.Logs import Log

file = os.path.basename(sys.argv[0])
log = Log(file, "E:\\suyhLogs\\submit.log")
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


def wait_flink_cluster_idle():
    while True:
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
    flink_cluster_idle = wait_flink_cluster_idle()
    print()




