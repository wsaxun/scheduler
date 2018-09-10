# scheduler接口文档
### 索引
1. <a href='#1'>增加interval类型备份任务接口</a>
2. <a href='#2'>修改interval类型备份任务接口</a>
3. <a href='#3'>暂停任务接口</a>
4. <a href='#4'>恢复任务接口</a>
5. <a href='#5'>删除任务接口</a>
6. <a href='#6'>查询任务接口</a>
---


### 增加interval类型备份任务<a name='1'></a>

###### 接口
> add_scheduler_start_backup_job_by_interval

###### 接口功能
> 增加interval类型的备份任务，开始备份时间为传递过来的start_time参数

###### 请求方式
> 通过nameko的rpc调用，服务名'scheduler'

###### 请求参数
|参数|必选|类型|说明|
|:---|:---|:---|:---|
|scheduler_id|True|str|scheduler id，全局唯一|
|policy_name|True|str|policy name|
|days|True|int|每隔多天执行一次|
|start_time|True|str|执行开始窗口， like '02:01'|
|duration|True|int|可以允许间隔|
|misfire_grace_time|True|int|恩惠时间，此时间为秒数。当调度器由于重启或者其他原因导致未能正常执行时，<br>正常情况下调度器本该执行n次，实际执行次数为misfire_grace_time/days的整数<br>|
|**url_kwargs|False||其他传递过来的关键字参数|

###### 返回参数
|参数|类型|说明|
|:---|:---|:---|
|status|str|状态， 'success' or 'fail'|
|description|str or dict|失败时返回str， 成功时返回dict，参数为：job_id,func,args,kwargs,misfire_grace_time,next_run_time|
|code|int|状态码|


### 修改interval类型备份任务接口<a name='2'></a>

###### 接口
> modify_start_backup_job_by_interval

###### 接口功能
> 修改interval类型的备份任务，开始备份时间为传递过来的start_time参数

###### 请求方式
> 通过nameko的rpc调用，服务名'scheduler'

###### 请求参数
|参数|必选|类型|说明|
|:---|:---|:---|:---|
|scheduler_id|True|str|scheduler id，全局唯一|
|policy_name|True|str|policy name|
|days|True|int|每隔多天执行一次|
|start_time|True|str|执行开始窗口， like '02:01'|
|duration|True|int|可以允许间隔|
|misfire_grace_time|True|int|恩惠时间，此时间为秒数。当调度器由于重启或者其他原因导致未能正常执行时，<br>正常情况下调度器本该执行n次，实际执行次数为misfire_grace_time/days的整数<br>|
|**url_kwargs|False||其他传递过来的关键字参数|

###### 返回参数
|参数|类型|说明|
|:---|:---|:---|
|status|str|状态， 'success' or 'fail'|
|description|str or dict|失败时返回str， 成功时返回dict，参数为：job_id,func,args,kwargs,misfire_grace_time,next_run_time|
|code|int|状态码|


### 暂停任务接口<a name='3'></a>

###### 接口
> pause_job

###### 接口功能
> 暂停指定scheduler的任务，对于当前时间点已经在执行的scheduler不会被暂停

###### 请求方式
> 通过nameko的rpc调用，服务名'scheduler'

###### 请求参数
|参数|必须|类型|说明|
|:--- |:---|:---|:--- |
|scheduler_id|True|str|scheduler的id|

###### 返回参数
|参数|类型|说明|
|:---|:---|:---|
|status|str|状态， 'success' or 'fail'|
|description|str or dict|失败时返回str， 成功时返回dict，参数为：job_id,func,args,kwargs,misfire_grace_time,next_run_time|
|code|int|状态码|


### 恢复任务接口<a name='4'></a>

###### 接口
> resume_job

###### 接口功能
> 恢复指定scheduler的任务，服务名'scheduler'

###### 请求方式
> 通过nameko的rpc调用

###### 请求参数
|参数|必须|类型|说明|
|:--- |:---|:---|:--- |
|scheduler_id|True|str|scheduler的id|

###### 返回参数
|参数|类型|说明|
|:---|:---|:---|
|status|str|状态， 'success' or 'fail'|
|description|str or dict|失败时返回str， 成功时返回dict，参数为：job_id,func,args,kwargs,misfire_grace_time,next_run_time|
|code|int|状态码|


### 删除任务接口<a name='5'></a>

###### 接口
> remove_job

###### 接口功能
> 删除指定scheduler的任务

###### 请求方式
> 通过nameko的rpc调用，服务名'scheduler'

###### 请求参数
|参数|必须|类型|说明|
|:--- |:---|:---|:--- |
|scheduler_id|True|str|scheduler的id|

###### 返回参数
|参数|类型|说明|
|:---|:---|:---|
|status|str|状态， 'success' or 'fail'|
|description|str or dict|失败时返回str， 成功时返回dict，参数为：job_id,func,args,kwargs,misfire_grace_time,next_run_time|
|code|int|状态码|


### 查询任务接口<a name='6'></a>

###### 接口
> get_job

###### 接口功能
> 查询指定scheduler id的任务

###### 请求方式
> 通过nameko的rpc调用，服务名'scheduler'

###### 请求参数
|参数|必须|类型|说明|
|:--- |:---|:---|:--- |
|scheduler_id|True|str|scheduler的id|

###### 返回参数
|参数|类型|说明|
|:---|:---|:---|
|status|str|状态， 'success' or 'fail'|
|description|str or dict|失败时返回str， 成功时返回dict，参数为：job_id,func,args,kwargs,misfire_grace_time,next_run_time|
|code|int|状态码|
