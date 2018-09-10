import apscheduler
from nameko.rpc import rpc
from .decorators import (check_start_backup_param, serialization_result)
from apscheduler.triggers.interval import IntervalTrigger
from .dependencies import Scheduler as DepScheduler
from .task import *


class Scheduler:
    name = 'scheduler'
    scheduler = DepScheduler()

    @staticmethod
    def _generator_id(policy_name):
        time_stamp = str(round(time.time() * 1000))
        scheduler_id = 'scheduler_' + policy_name + '_' + time_stamp
        return scheduler_id

    @staticmethod
    def _execute_scheduler(func, *args, **kwargs):
        """
        fetchall exception when we call scheduler object
        :param func: object
        :return: dict
        """
        try:
            result = func(*args, **kwargs)
        except apscheduler.jobstores.base.ConflictingIdError as e:
            return {'status': 'fail', 'description': e.__str__(), 'code': 500}
        except (apscheduler.schedulers.SchedulerAlreadyRunningError,
                apscheduler.schedulers.SchedulerNotRunningError):
            return {'status': 'fail',
                    'description': 'scheduler not running or scheduler running error',
                    'code': 500
                    }
        except apscheduler.executors.base.MaxInstancesReachedError as e:
            return {'status': 'fail', 'description': e.__str__(), 'code': 500}
        except Exception as e:
            return {'status': 'fail', 'description': e.__str__(), 'code': 500}
        return {'status': 'success', 'description': result, 'code': 200}

    # @staticmethod
    # def _generator_trigger(cron):
    #     return CronTrigger.from_crontab(cron)

    @staticmethod
    def _generator_trigger(days):
        return IntervalTrigger(days=days)

    @staticmethod
    def _generator_first_running_time(start_time):
        now = datetime.now()
        first_run_time = datetime.strptime(
            '{0}-{1}-{2} {3}:{4}'.format(now.year, now.month, now.day,
                                         start_time.strip().split(':')[0],
                                         start_time.strip().split(':')[1]),
            '%Y-%m-%d %H:%M')
        if first_run_time < now:
            first_run_time = first_run_time + timedelta(days=1)
        return first_run_time

    @staticmethod
    def _generator_kwargs(policy_name, duration, start_time, url_kwargs):
        kwargs = dict(policy_name=policy_name, duration=duration,
                      start_time=start_time)
        kwargs = dict(kwargs, **url_kwargs)
        return kwargs

    # @serialization_result
    # @check_start_backup_param
    # @rpc
    # def add_scheduler_start_backup_job(self, policy_name, cron=None,
    #                                    start_time=None, duration=None,
    #                                    misfire_grace_time=None, **url_kwargs):
    #     """
    #     add scheduler start_backup job by cron
    #     :param cron: str like linux cron , '*/2 * * * *'
    #     :param duration: int
    #     :param start_time: str like '01:00'
    #     :param policy_name: str
    #     :param misfire_grace_time: int
    #     :param url_kwargs:
    #     :return: dict
    #     """
    #     scheduler_id = self._generator_id(policy_name)
    #     trigger = self._generator_trigger(cron)
    #     kwargs = self._generator_kwargs(policy_name, duration,
    #                                     start_time, url_kwargs)
    #     scheduler_result = self._execute_scheduler(scheduler.add_job,
    #                                                start_backup, id=scheduler_id,
    #                                                trigger=trigger,
    #                                                misfire_grace_time=misfire_grace_time,
    #                                                kwargs=kwargs)
    #     return scheduler_result
    #
    # @serialization_result
    # @check_start_backup_param
    # @rpc
    # def modify_start_backup_job(self, scheduler_id, policy_name=None, cron=None,
    #                             start_time=None, duration=None,
    #                             misfire_grace_time=None,
    #                             **url_kwargs):
    #     """
    #     modify scheduler job by job' id
    #     :param scheduler_id: str
    #     :param policy_name: str
    #     :param cron: str
    #     :param duration: int
    #     :param start_time: str like '00:01'
    #     :param misfire_grace_time: int
    #     :param url_kwargs: dict
    #     :return: dict
    #     """
    #     trigger = self._generator_trigger(cron)
    #     kwargs = self._generator_kwargs(policy_name, duration,
    #                                     start_time, url_kwargs)
    #     scheduler_result = self._execute_scheduler(scheduler.modify_job,
    #                                                scheduler_id,
    #                                                trigger=trigger,
    #                                                misfire_grace_time=misfire_grace_time,
    #                                                kwargs=kwargs)
    #     return scheduler_result

    @serialization_result
    @check_start_backup_param
    @rpc
    def add_scheduler_start_backup_job_by_interval(self, scheduler_id,
                                                   policy_name,
                                                   days=None,
                                                   start_time=None,
                                                   duration=None,
                                                   misfire_grace_time=None,
                                                   **url_kwargs):
        """
        add scheduler start_backup job by cron
        :param scheduler_id: str
        :param days: int
        :param duration: int
        :param start_time: str like '01:00'
        :param policy_name: str
        :param misfire_grace_time: int
        :param url_kwargs:
        :return: dict
        """
        print(self.scheduler)
        trigger = self._generator_trigger(days)
        kwargs = self._generator_kwargs(policy_name, duration,
                                        start_time, url_kwargs)
        first_run_time = self._generator_first_running_time(start_time)
        scheduler_result = self._execute_scheduler(self.scheduler.add_job,
                                                   start_backup,
                                                   id=scheduler_id,
                                                   trigger=trigger,
                                                   next_run_time=first_run_time,
                                                   misfire_grace_time=misfire_grace_time,
                                                   kwargs=kwargs)
        return scheduler_result

    @serialization_result
    @check_start_backup_param
    @rpc
    def modify_start_backup_job_by_interval(self, scheduler_id,
                                            policy_name=None,
                                            days=None,
                                            start_time=None, duration=None,
                                            misfire_grace_time=None,
                                            **url_kwargs):
        """
        modify scheduler job by job' id
        :param scheduler_id: str
        :param policy_name: str
        :param days: int
        :param duration: int
        :param start_time: str like '00:01'
        :param misfire_grace_time: int
        :param url_kwargs: dict
        :return: dict
        """
        trigger = self._generator_trigger(days)
        kwargs = self._generator_kwargs(policy_name, duration,
                                        start_time, url_kwargs)
        first_run_time = self._generator_first_running_time(start_time)
        scheduler_result = self._execute_scheduler(self.scheduler.modify_job,
                                                   scheduler_id,
                                                   trigger=trigger,
                                                   next_run_time=first_run_time,
                                                   misfire_grace_time=misfire_grace_time,
                                                   kwargs=kwargs)
        return scheduler_result

    @serialization_result
    @rpc
    def pause_job(self, scheduler_id):
        """
        pause job by job's id
        :param scheduler_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(self.scheduler.pause_job,
                                                   scheduler_id)
        return scheduler_result

    @serialization_result
    @rpc
    def resume_job(self, scheduler_id):
        """
        resume job by job' id
        :param scheduler_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(self.scheduler.resume_job,
                                                   scheduler_id)
        return scheduler_result

    @rpc
    def remove_job(self, scheduler_id):
        """
        remove job by job's id
        :param scheduler_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(self.scheduler.remove_job,
                                                   scheduler_id)
        return scheduler_result

    @serialization_result
    @rpc
    def get_job(self, scheduler_id):
        """
        get some jobs by job's id
        :param scheduler_id: str
        :return: dict
        """
        scheduler_result = self._execute_scheduler(self.scheduler.get_job,
                                                   scheduler_id)
        return scheduler_result

    @serialization_result
    @rpc
    def get_jobs(self):
        """
        get all jobs
        :return: dict
        """
        scheduler_result = self._execute_scheduler(self.scheduler.get_jobs)
        return scheduler_result
