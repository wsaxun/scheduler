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
        print({'status': 'fail', 'msg': 'can not execute at this time'})
        return {'status': 'fail', 'msg': 'can not execute at this time'}
    url_kwargs.update(policy_name=policy_name)
    try:
        response = requests.post(start_backup_url, data=url_kwargs,
                                 timeout=request_timeout)
        if not 200 <= response.status_code <= 399:
            print({'status': 'fail', 'msg': 'remote host execute error'})
            return {'status': 'fail', 'msg': 'remote host execute error'}
        result = {'status': 'success', 'data': response.json()}
    except requests.exceptions.ConnectTimeout:
        print({'status': 'fail',
               'msg': 'ConnectTimeout {0} seconds'.format(request_timeout)})
        return {'status': 'fail',
                'msg': 'ConnectTimeout {0} seconds'.format(request_timeout)}
    except Exception:
        print({'status': 'fail', 'msg': 'unknown error'})
        return {'status': 'fail', 'msg': 'unknown error'}

    print(datetime.now())
    print(result)
    return result


def del_backup(*args, **kwargs):
    print(datetime.now())
