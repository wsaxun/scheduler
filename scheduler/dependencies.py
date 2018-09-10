import logging
from apscheduler.schedulers.background import BackgroundScheduler
from nameko.extensions import DependencyProvider
from schedulerConfig import job_stores, executors, job_defaults


class Scheduler(DependencyProvider):
    def setup(self):
        logging.getLogger('apscheduler.executors.default').setLevel(
            logging.WARNING)
        scheduler = BackgroundScheduler(jobstores=job_stores,
                                        executors=executors,
                                        job_defaults=job_defaults)
        setattr(self, 'scheduler', scheduler)
        self.scheduler.start()

    def get_dependency(self, worker_ctx):
        return self.scheduler

    def stop(self):
        self.scheduler.shutdown()
