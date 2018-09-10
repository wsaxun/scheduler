from functools import wraps
from apscheduler.job import Job
from .schedulerConfig import misfire


def serialization_result(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        def serialization_one_job_or_job_list(job_data, status, code):
            next_run_time = None
            job_result = {'status': status, 'code': code}
            if isinstance(job_data, Job):
                if job_data.next_run_time:
                    next_run_time = job_data.next_run_time.strftime(
                        '%Y-%m-%d %H:%M:%S')
                job = dict(job_id=job_data.id,
                           func=job_data.func.__name__,
                           args=job_data.args,
                           kwargs=job_data.kwargs,
                           misfire_grace_time=job_data.misfire_grace_time,
                           next_run_time=next_run_time)
                job_result.update(description=job)
                return job_result
            serializer_data = []
            for one_job in job_data:
                if isinstance(one_job, Job):
                    if one_job.next_run_time:
                        next_run_time = one_job.next_run_time.strftime(
                            '%Y-%m-%d %H:%M:%S')
                    job = dict(job_id=one_job.id,
                               func=one_job.func.__name__,
                               args=one_job.args,
                               kwargs=one_job.kwargs,
                               misfire_grace_time=one_job.misfire_grace_time,
                               next_run_time=next_run_time)
                    serializer_data.append(job)
                else:
                    serializer_data.append(one_job)
                job_result.update(description=serializer_data)
            return job_result

        result = func(self, *args, **kwargs)
        if result['status'] == 'fail' or result['status'] != 'success':
            new_result = result
            return new_result
        if not result['description']:
            new_result = dict(status=result['status'])
        elif isinstance(result['description'], list) or isinstance(
                result['description'],
                Job):
            new_result = serialization_one_job_or_job_list(
                result['description'],
                result['status'], result['code'])
            return new_result
        else:
            new_result = result
        return new_result

    return inner


# def check_start_backup_param(func):
#     @wraps(func)
#     def inner(self, *args, **kwargs):
#         if not args:
#             return {'status': 'fail', 'description': 'position args is null',
#                     'code': 400}
#         if not kwargs.get('duration'):
#             return {'status': 'fail', 'description': 'not duration args',
#                     'code': 400}
#         if not kwargs.get('start_time'):
#             return {'status': 'fail', 'description': 'not start_time args',
#                     'code': 400}
#         if not kwargs.get('cron'):
#             return {'status': 'fail', 'description': 'not cron args',
#                     'code': 400}
#         # TODO
#         misfire_grace_time = kwargs.get('misfire_grace_time')
#         if not misfire_grace_time:
#             misfire_grace_time = int(misfire * 60 * 60 * 24)
#         kwargs['misfire_grace_time'] = misfire_grace_time
#         print(args)
#         print(kwargs)
#         result = func(self, *args, **kwargs)
#         return result
#
#     return inner


def check_start_backup_param(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if not args:
            return {'status': 'fail', 'description': 'position args is null',
                    'code': 400}
        if not kwargs.get('duration'):
            return {'status': 'fail', 'description': 'not duration args',
                    'code': 400}
        if not kwargs.get('start_time'):
            return {'status': 'fail', 'description': 'not start_time args',
                    'code': 400}
        # TODO
        misfire_grace_time = kwargs.get('misfire_grace_time')
        if not misfire_grace_time:
            misfire_grace_time = int(misfire * 60 * 60 * 24)
        kwargs['misfire_grace_time'] = misfire_grace_time
        result = func(self, *args, **kwargs)
        return result

    return inner
