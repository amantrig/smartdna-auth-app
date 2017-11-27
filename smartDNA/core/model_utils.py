import time
import datetime,os,sys
os.environ['PYTHON_EGG_CACHE'] = "/tmp"
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH+'smartDNA/'
if path not in sys.path:
    sys.path.append(path)
path = PROJECT_PATH
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'

from django.db.models.loading import get_model
from django.conf import settings
from core.models import Deployment

WORK_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]+'smartDNA/'
def identify_noise(Verification,asset_code,scan_time):
    sctm=datetime.datetime.strptime(scan_time,'%Y-%m-%d %H:%M:%S')
    if Verification.objects.filter(asset_code__iexact=asset_code,status=3,scan_time__gt=sctm-datetime.timedelta(seconds=30)).count()>0:
     vrns=Verification.objects.filter(asset_code__iexact=asset_code,status=3,scan_time__gt=sctm-datetime.timedelta(seconds=30)).order_by('-scan_time')
     for ver_obj in vrns:
	ver_obj.status = 13
        ver_obj.save()

def tamp_state(Verification,asset_code,d1,d2,d3,h1,h2,h3):
    status=3
    if Verification.objects.filter(asset_code__iexact=asset_code,status=14).count()>0:
     ver_objs=Verification.objects.filter(asset_code__iexact=asset_code,status=3).order_by('-scan_time')
     ver_obj=ver_objs[0]
     if ver_obj.d1==d1 and ver_obj.d2==d2 and ver_obj.d3==d3 and ver_obj.h1==h1 and ver_obj.h2==h2 and ver_obj.h3==h3:
	status=14
     else:	      
	status=15
    elif Verification.objects.filter(asset_code__iexact=asset_code,status=3).count()>0:
     ver_objs=Verification.objects.filter(asset_code__iexact=asset_code,status=3).order_by('-scan_time')
     ver_obj=ver_objs[0]
     if ver_obj.d1==d1 and ver_obj.d2==d2 and ver_obj.d3==d3 and ver_obj.h1==h1 and ver_obj.h2==h2 and ver_obj.h3==h3:
	status=3
     else:	      
	status=14
    else:
	status=3
    return status

def precision_test(asset_code,dep_path,precision):
    Verification = get_model(dep_path, 'Verification')
    i=0
    rvs=Verification.objects.filter(asset_code=asset_code,status=1)
    if rvs.count()>0:
     print "total registration records ",rvs.count()
     d1=float(rvs[0].d1)
     d2=float(rvs[0].d2)
     d3=float(rvs[0].d3)
     vvs=Verification.objects.filter(asset_code=asset_code,status=2)
     if vvs.count()>0:
      print "total verification records ",vvs.count()
      for vv in vvs:
       if (abs(d1-float(vv.d1))<float(precision) or abs(d2-float(vv.d2))<float(precision) or abs(d3-float(vv.d3))<float(precision)):
        print "precise matches at scan time: ",vv.scan_time
        i=i+1
    print "Total precise mathces under precision ",precision," verification records ",i 

