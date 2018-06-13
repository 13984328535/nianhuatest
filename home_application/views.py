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
from home_application.models import MultRecode
import os  
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail_smtp(text):
    sender = '13984328535@139.com'
    receivers = ['13984328535@139.com']
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header(u"13984328535@139.com系统监控", 'utf-8')
    message['To'] =  Header(u"13984328535@139.com", 'utf-8')
    message['Subject'] = Header('重要:系统监控告警', 'utf-8').encode() 

    try:
        smtp = smtplib.SMTP('smtp.139.com', 25) 
        #smtp.connect() 
        #smtp.set_debuglevel(1)
        smtp.login('13984328535', 'anling') 
        smtp.sendmail(sender, receivers, message.as_string()) 
        smtp.quit()
        return True
    except smtplib.SMTPException:
        return False

def send_mail(request):
    host_name = request.POST.get('host_name')
    host_time = request.POST.get('host_time')
    text = u'主机名: %s, 故障时间: %s, 请尽快处理.' % (host_name,host_time) 
    text = text.replace('&nbsp;', ' ')
    if send_mail_smtp(text):
        return  render_json({'result':True})
    else:
        render_json({'result':False})

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
    
def index(request):
    return HttpResponse('Hello World')

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
