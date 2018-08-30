from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import pymysql

pymysql.install_as_MySQLdb()

job_stores = {
    'default': SQLAlchemyJobStore(
        url='mysql+mysqldb://root:123456@172.17.0.4/myscheduler')
}
executors = {
    'default': ThreadPoolExecutor(50),
    'process_pool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 2
}

# 100%
misfire = 1

# start_backup url
# start_backup_url = 'https://www.httpbin.org/post'
start_backup_url = 'http://google.com'

# request timeout
request_timeout = 5
