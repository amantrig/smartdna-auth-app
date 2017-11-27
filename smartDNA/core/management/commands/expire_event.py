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

from django.core.management.base import BaseCommand, CommandError
from core.models import Deployment,Logger
import datetime
from core.models import Configuration
def get_expiry_days():
    days=90
    cobj=Configuration.objects.filter(dep_name=1)[0]
    days=cobj.cleanup_interval
    #with open(PROJECT_PATH+'smartDNA/media/expiry_time.json', 'r') as f:
    # json_data = json.load(f)
    # days=json_data['days']
    return days

days=get_expiry_days()

def deleteVerification():
    from django.db.models.loading import get_model
    q=Deployment.objects.values('dep_path').distinct()
    for index in range(q.count()):
     dep_path=q[index]['dep_path']
     Verification = get_model(dep_path, 'Verification')
     print Verification.objects.filter(scan_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days)),status=2).count()," verification record deleted successfuly"
     Verification.objects.filter(scan_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days)),status=2).delete()

def deletePostmortemImage():
    from django.db.models.loading import get_model
    q=Deployment.objects.values('dep_path').distinct()
    for index in range(q.count()):
     dep_path=q[index]['dep_path']
     PostmortemImage = get_model(dep_path, 'PostmortemImage')
     print PostmortemImage.objects.filter(scan_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).count()," postmortem record deleted successfuly"
     PostmortemImage.objects.filter(scan_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).delete()

def deleteAnomaly():
    from django.db.models.loading import get_model
    q=Deployment.objects.values('dep_path').distinct()
    for index in range(q.count()):
     dep_path=q[index]['dep_path']
     Anomaly = get_model(dep_path, 'Anomaly')
     print Anomaly.objects.filter(scan_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).count()," anomaly record deleted successfuly"
     Anomaly.objects.filter(scan_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).delete()

def deleteAlert():
    from django.db.models.loading import get_model
    q=Deployment.objects.values('dep_path').distinct()
    for index in range(q.count()):
     dep_path=q[index]['dep_path']
     Alert = get_model(dep_path, 'Alert')
     print Alert.objects.filter(alert_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).count()," alert record deleted successfuly"
     Alert.objects.filter(alert_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).delete()

def deleteLogger():
    print Logger.objects.filter(login_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).count()," login record deleted successfuly"
    Logger.objects.filter(login_time__lt=datetime.datetime.now()-datetime.timedelta(days=int(days))).delete()

class Command(BaseCommand):
    help = 'Delete all the rocords which are older than 7 days'
    def handle(self, *args, **options):
        deleteVerification()
        deletePostmortemImage()
        deleteAnomaly()
        deleteAlert()
        deleteLogger()
