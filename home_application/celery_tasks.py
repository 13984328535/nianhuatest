# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from common.log import logger
from home_application.models import PortScanPara
from threading import Thread


@task()
def async_portscan():
    logger.error(u"celery 定时任务执行成功，async_portscan")
    last_scantask = PortScanPara.objects.filter().last()
    host = hostname(); 
    
    source_hostname = last_scantask.source_hostname
    target_ip = last_scantask.target_ip
    target_port = last_scantask.target_port
    
    if(source_hostname != ""):
        if(host != source_hostname):
            return
    if(target_ip == ""):
        return
    if(target_port == ""):
        target_port = "7001,8443,8081,8888,9092,2181,10004,9300,8443,8008,8029,8010,8009,8019,6379,16379,3306,6380,10011,10021,10031,13031,48669,5672,15672,25672,59313,50002,48534,58725,58636,58625,58725,58636,58625,48669,48673,48668,59313,52025,52030,443,4245,10050,10051,10052,10053,10054,10041,10042,10043,10044,5260,8500,10050,10051,10052,10053,10054,10055,10056,13021,13031,13041,13051,31001,31002,31003,31004,31005,32001,32002,32003,32004,32005,33031,33062,33083,27017"
        
    target_ports = str(target_port).split(',')
    for target_port in target_ports:
        t = Thread(target = nmapScan,args = (str(host), str(target_ip), str(target_port)))
        t.start()      

@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))
    