import logging
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from nameko.rpc import rpc
from schedulerConfig import job_stores, executors, job_defaults
from decorators import (check_start_backup_param, serialization_result)
from task import *

scheduler = BackgroundScheduler(jobstores=job_stores,
                                executors=executors,
                                job_defaults=job_defaults)
scheduler.start()
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)


class Scheduler:
    name = 'scheduler'

    @staticmethod
    def _generator_id(policy_name):
        time_stamp = str(round(time.time() * 1000))
        job_id = 'scheduler_' + policy_name + '_' + time_stamp
        return job_id

    @staticmethod
    def _execute_scheduler(func, *args, **kwargs):
        """
        fetchall exception when we call scheduler object
        :param func: object
        :return: dict
        """
        print(args)
        print(kwargs)
        try:
            result = func(*args, **kwargs)
        except apscheduler.jobstores.base.ConflictingIdError as e:
            return {'status': 'fail', 'msg': e.__str__()}
        except (apscheduler.schedulers.SchedulerAlreadyRunningError,
                apscheduler.schedulers.SchedulerNotRunningError):
            return {'status': 'fail',
                    'msg': 'scheduler not running or scheduler running error'}
        except apscheduler.executors.base.MaxInstancesReachedError as e:
            return {'status': 'fail', 'msg': e.__str__()}
        except Exception as e:
            return {'status': 'fail', 'msg': e.__str__()}
        return {'status': 'success', 'data': result}

    @staticmethod
    def _generator_trigger(cron):
        return CronTrigger.from_crontab(cron)

    @staticmethod
    def _generator_kwargs(policy_name, duration, start_time, url_kwargs):
        kwargs = dict(policy_name=policy_name, duration=duration,
                      start_time=start_time)
        kwargs = dict(kwargs, **url_kwargs)
        return kwargs

    @serialization_result
    @check_start_backup_param
    @rpc
    def add_scheduler_start_backup_job(self, policy_name, cron=None,
                                       duration=None, start_time=None,
                                       misfire_grace_time=None, **url_kwargs):
        """
        add scheduler start_backup job by cron
        :param cron: str like linux cron , '*/2 * * * *'
        :param duration: int
        :param start_time: str like '01:00'
        :param policy_name: str
        :param misfire_grace_time: int
        :param url_kwargs:
        :return: dict
        """
        job_id = self._generator_id(policy_name)
        trigger = self._generator_trigger(cron)
        kwargs = self._generator_kwargs(policy_name, duration,
                                        start_time, url_kwargs)
        scheduler_result = self._execute_scheduler(scheduler.add_job,
                                                   start_backup, id=job_id,
                                                   trigger=trigger,
                                                   misfire_grace_time=misfire_grace_time,
                                                   kwargs=kwargs)
        return scheduler_result

    @serialization_result
    @check_start_backup_param
    @rpc
    def modify_start_backup_job(self, job_id, policy_name=None, cron=None,
                                duration=None, start_time=None,
                                misfire_grace_time=None,
                                **url_kwargs):
        """
        modify scheduler job by job' id
        :param job_id: str
        :param policy_name: str
        :param cron: str
        :param duration: int
        :param start_time: str like '00:01'
        :param misfire_grace_time: int
        :param url_kwargs: dict
        :return: dict
        """
        trigger = self._generator_trigger(cron)
        kwargs = self._generator_kwargs(policy_name, duration,
                                        start_time, url_kwargs)
        scheduler_result = self._execute_scheduler(scheduler.modify_job, job_id,
                                                   trigger=trigger,
                                                   misfire_grace_time=misfire_grace_time,
                                                   kwargs=kwargs)
        return scheduler_result

    @serialization_result
    @rpc
    def pause_job(self, job_id):
        """
        pause job by job's id
        :param job_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(scheduler.pause_job, job_id)
        return scheduler_result

    @serialization_result
    @rpc
    def resume_job(self, job_id):
        """
        resume job by job' id
        :param job_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(scheduler.resume_job, job_id)
        return scheduler_result

    @rpc
    def remove_job(self, job_id):
        """
        remove job by job's id
        :param job_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(scheduler.remove_job, job_id)
        return scheduler_result

    @serialization_result
    @rpc
    def get_job(self, job_id):
        """
        get some jobs by job's id
        :param job_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(scheduler.get_job, job_id)
        return scheduler_result

    @serialization_result
    @rpc
    def get_jobs(self):
        """
        get all jobs
        :return: dict
        """
        scheduler_result = self._execute_scheduler(scheduler.get_jobs)
        return scheduler_result
