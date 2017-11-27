import os
import sys

os.environ['PYTHON_EGG_CACHE'] = "/tmp"
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH+'smartDNA/'
if path not in sys.path:
    sys.path.append(path)
path = '/home/smartdna/linksmart/'
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'
import datetime

depn=os.path.dirname(os.path.realpath(__file__)).split("/")[len(os.path.dirname(os.path.realpath(__file__)).split("/"))-1]
from django.db.models.loading import get_model


def count_in_range(from_last):
    Verification=get_model(depn,'Verification')
    vdata=Verification.objects.filter(scan_time__range=(from_last, datetime.datetime.now())).order_by('-scan_time')
    c = str(vdata.count())
    print c

def update_column(from_last,location,geo_location):
    Verification=get_model(depn,'Verification')
    field_dict = {'location':location,'geo_location':geo_location}
    vdata=Verification.objects.filter(scan_time__range=(from_last, datetime.datetime.now())).order_by('-scan_time')
    #vdata.location=location
    #vdata.geo_location=geo_location
    vdata.update(**field_dict)
    print str(vdata.count())," records updated to:",location
