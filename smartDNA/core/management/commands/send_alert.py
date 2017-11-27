import os
import sys
import json
os.environ['PYTHON_EGG_CACHE'] = "/tmp"

PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH+'smartDNA/'
if path not in sys.path:
    sys.path.append(path)
path = PROJECT_PATH
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from core.models import Deployment
from core.utils import get_email_connection
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def html_table(asset_list):
  yield '<h4>====Assets mentioned below not scanned as per schedule====</h4>'
  yield '<table>'
  for sublist in asset_list:
    yield '<tr style="border: 1px solid black;"><td style="color:red;">%s</td></tr>'%(sublist)
  yield '</table>'

def send_alert():
   connection=get_email_connection()
   q=Deployment.objects.values('dep_path').distinct()
   for index in range(q.count()):
    dep_path=q[index]['dep_path']
    Verification = get_model(dep_path, 'Verification')
    PeriodicScanAsset = get_model(dep_path, 'PeriodicScanAsset')
    asset_list=[]
    psa=PeriodicScanAsset.objects.all()
    for p in psa:
     asset_code= p.asset_code
     nm= int(p.interval)*60
     ex= datetime.now() - timedelta(minutes=nm)
     if Verification.objects.filter(asset_code=asset_code,scan_time__gte=ex).count()<1:
      asset_list.append(asset_code)
    #print asset_list,len(asset_list)
    AlertSubscriber= get_model(dep_path, 'AlertSubscriber')
    scr_list= [scr.email for scr in AlertSubscriber.objects.filter(scr_status='Active')]
    text_content = 'Assets mentioned below not scanned as per schedule.'
    #print ''.join(html_table(asset_list))
    html_content = ''.join(html_table(asset_list))
    print html_content
    msg = EmailMultiAlternatives("Periodic scan alert", text_content, settings.EMAIL_HOST_USER, scr_list,connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class Command(BaseCommand):
    help = 'Create group with specified permissions'
    def handle(self, *args, **options):
      send_alert()
	
