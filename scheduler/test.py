from threading import Thread
import uuid
from nameko.standalone.rpc import ClusterRpcProxy
import time


class Test(Thread):
    def __init__(self):
        super(Test, self).__init__()
        self.config = {
            'AMQP_URI': 'pyamqp://guest:guest@172.17.0.3'
        }

    def run(self):
        while True:
            sched_id = uuid.uuid1()
            policy_name = 'xums'
            days = 1
            start_time = '02:00'
            duration = 2
            with ClusterRpcProxy(self.config) as rpc:
                result = rpc.scheduler.add_scheduler_start_backup_job_by_interval(
                    sched_id,
                    policy_name,
                    days=days,
                    start_time=start_time,
                    duration=duration)
                print(result)


if __name__ == '__main__':
    for i in range(10):
        test = Test()
        test.setDaemon(True)
        test.start()
    n = 0
    while n < 1000:
        time.sleep(10)
        n += 1
