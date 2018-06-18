# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from common.mymako import render_mako_context, render_json
#from django.http import JsonResponse   同render_json
from home_application.models import MultRecode, PortScan, PortScanPara
import os  
import time
import json
import nmap
from threading import Thread
from test.test_sax import start


def get_scan_records(request):
    nowTime = request.POST.get('nowTime')
    nowTime = nowTime.replace('&nbsp;', ' ')
    #all_record = PortScan.objects.all().order_by('scan_time')
    all_record = PortScan.objects.filter(scan_time__gt=nowTime).order_by('scan_time')
    records = []  
    for record in all_record:  
        records.append({'source_hostname':record.source_hostname,'target_ip':record.target_ip,'target_port':record.target_port,'state':record.state,'protocol':record.protocol,'scan_time':str(record.scan_time)})  
    scan_records = json.dumps(records) 
    return render_json({'result':True, 'all_record':scan_records})

    

def get_api(api_url, token):
    url = "%s%s" % (settings.BK_PAAS_HOST, api_url)
    textmod ={'bk_app_code':settings.APP_ID,
    'bk_app_secret':settings.APP_TOKEN,
    'bk_token':token }
    textmod = urllib.urlencode(textmod)

    req = urllib2.Request(url = '%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    res = res.read()
    return res;

def hosttime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def hostname():
    #hostname = socket.gethostname()
    #print hostname    
    sys = os.name  
    if sys == 'nt':  
        hostname = os.getenv('computername')  
        return hostname  
    elif sys == 'posix':  
        host = os.popen('echo $HOSTNAME')  
        try:  
            hostname = host.read()  
            return hostname  
        finally:  
            host.close()  
    else:  
        return 'Unkwon hostname'        

def nmapScan(hostname,tip, port):
    nmScan = nmap.PortScanner()
    nmScan.scan(tip, port)
    state = nmScan[tip]['tcp'][int(port)]['state']
    #print "[*] "+tip+"tcp/"+port+" "+state
    portscan_recode = PortScan(source_hostname=hostname, target_ip=tip, target_port=port,state=state,protocol="TCP")
    portscan_recode.save()
    
def portscan(request):
    source_hostname = request.POST.get('source_hostname')
    target_ip = request.POST.get('target_ip')
    target_port = request.POST.get('target_port')
    host = hostname();
    PortScan.objects.filter().delete();
    PortScanPara.objects.filter().delete();
    PortScanPara.objects.create(source_hostname=source_hostname,target_ip=target_ip,target_port=target_port,protocol="TCP",opere_hostname="")
    
#     if(source_hostname != ""):
#         if(host != source_hostname):
#             return
#     if(target_ip == ""):
#         return
#     if(target_port == ""):
#         target_port = "7001,8443,8081,8888,9092,2181,10004,9300,8443,8008,8029,8010,8009,8019,6379,16379,3306,6380,10011,10021,10031,13031,48669,5672,15672,25672,59313,50002,48534,58725,58636,58625,58725,58636,58625,48669,48673,48668,59313,52025,52030,443,4245,10050,10051,10052,10053,10054,10041,10042,10043,10044,5260,8500,10050,10051,10052,10053,10054,10055,10056,13021,13031,13041,13051,31001,31002,31003,31004,31005,32001,32002,32003,32004,32005,33031,33062,33083,27017"
#     target_ports = str(target_port).split(',')
#     for target_port in target_ports:
#         t = Thread(target = nmapScan,args = (str(host), str(target_ip), str(target_port)))
#         t.start()
    return render_json({'result':True})

    

def multiplication_computer(request):
    multiplier = int(request.POST.get('multiplier'))
    multiplicand = int(request.POST.get('multiplicand'))
    mult_result = multiplier * multiplicand
    mult_recode = MultRecode(multiplier=multiplier, multiplicand=multiplicand, mult_result=mult_result)
    mult_recode.save()
    host_name = hostname();
    host_time = hosttime();
    return render_json({'result':True, 'mult_result':mult_result, 'host_name':host_name, 'host_time':host_time})

def home(request):
    """
    首页
    """
    all_record = MultRecode.objects.all()
    ctx = {
        'all_record': all_record
    }
    return render_mako_context(request, '/home_application/home.html',ctx)


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')
