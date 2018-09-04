from datetime import datetime, timedelta
import time
import requests
from functools import wraps
from schedulerConfig import start_backup_url, request_timeout


def retry(retry_num=3, delay=5):
    def wrap(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 1
            result = None
            while n <= retry_num:
                result = func(*args, **kwargs)
                if result.get('status') == 'success':
                    break
                else:
                    time.sleep(delay)
                    n += 1
                    now = datetime.now()
                    min_time = datetime.strptime(
                        '{0}-{1}-{2} {3}:{4}'.format(now.year, now.month,
                                                     now.day,
                                                     kwargs.get(
                                                         'start_time').strip().split(
                                                         ':')[0],
                                                     kwargs.get(
                                                         'start_time').strip().split(
                                                         ':')[1]),
                        '%Y-%m-%d %H:%M')
                    max_time = min_time + timedelta(
                        hours=kwargs.get('duration'))
                    if not min_time <= now <= max_time:
                        break
            return result

        return inner

    return wrap


@retry(3, 5)
def start_backup(*args, duration=None, start_time=None, policy_name=None,
                 **url_kwargs):
    """
    start backup , it will check if the current time is the time that can be
    executed
    :param args:
    :param duration: int
    :param start_time: str, like '01:02'
    :param policy_name: str
    :param url_kwargs: **url_kwargs will pass to start_backup_url
    :return: dict
    """
    now = datetime.now()
    min_time = datetime.strptime(
        '{0}-{1}-{2} {3}:{4}'.format(now.year, now.month, now.day,
                                     start_time.strip().split(':')[0],
                                     start_time.strip().split(':')[1]),
        '%Y-%m-%d %H:%M')
    max_time = min_time + timedelta(hours=duration)
    if not min_time <= now <= max_time:
        print({'status': 'fail', 'description': 'can not execute at this time',
               'code': 500})
        return {'status': 'fail', 'description': 'can not execute at this time',
                'code': 500}
    url_kwargs.update(policy_name=policy_name)
    try:
        response = requests.post(start_backup_url, data=url_kwargs,
                                 timeout=request_timeout)
        if not 200 <= response.status_code <= 399:
            print({'status': 'fail', 'description': 'remote host execute error',
                   'code': 500})
            return {'status': 'fail',
                    'description': 'remote host execute error', 'code': 500}
        result = {'status': 'success', 'description': response.json()}
    except requests.exceptions.ConnectTimeout:
        print({'status': 'fail',
               'description': 'ConnectTimeout {0} seconds'.format(
                   request_timeout), 'code': 500})
        return {'status': 'fail',
                'description': 'ConnectTimeout {0} seconds'.format(
                    request_timeout), 'code': 500}
    except Exception:
        print({'status': 'fail', 'description': 'unknown error', 'code': 500})
        return {'status': 'fail', 'description': 'unknown error', 'code': 500}

    print(datetime.now())
    print(result)
    return result


def del_backup(*args, **kwargs):
    print(datetime.now())
