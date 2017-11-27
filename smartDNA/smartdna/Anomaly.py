__author__ = 'linksmart'
import re
import os
import sys

os.environ['PYTHON_EGG_CACHE'] = "/tmp"
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH+'smartDNA/'
if path not in sys.path:
    sys.path.append(path)
path = PROJECT_PATH
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'

from datetime import datetime, timedelta
depn=os.path.dirname(os.path.realpath(__file__)).split("/")[-1]
from django.db.models.loading import get_model
Verification=get_model(depn,'Verification')

def isAnomaly(asset_code):
    isAnomaly=False
    time_threshold = datetime.now() - timedelta(seconds=300)
    results = Verification.objects.filter(asset_code=asset_code,status=3,scan_time__gte=time_threshold)
    if results.count()>1:
	isAnomaly=True
    return isAnomaly
	
#isAnomaly(80122)
