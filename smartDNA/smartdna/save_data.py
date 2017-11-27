import os,sys
os.environ['PYTHON_EGG_CACHE'] = "/tmp"
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH+'smartDNA/'
if path not in sys.path:
    sys.path.append(path)
path = PROJECT_PATH
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'

depn=os.path.dirname(os.path.realpath(__file__)).split("/")[len(os.path.dirname(os.path.realpath(__file__)).split("/"))-1]
from django.db.models.loading import get_model
from django.utils.importlib import import_module
upload_data = import_module(depn+'.upload_data')
syncdata = upload_data.syncdata
from core.utils import send_confirmation

def saveData(asset_code,scan_time,time_millis,credential,orrcredential,d1,d2,d3,h1,h2,h3,angle,status,status_code,geoLoc,street,locality,city,state,postal_code,country,operator,username,password,scan_auth,productDetails,bit_mask,color_profile,image,email_id,company_name):
    #print status,company_name
    model_name='Verification'
    if status=='Registered':
      model_name='Registration'
    Verification=get_model(depn,model_name)
    v=Verification(asset_code=asset_code,
                      scan_time=scan_time,
                      credential=credential,
                      orr_credential=orrcredential,
                      d1=d1,
                      d2=d2,
                      d3=d3,
                      h1=h1,
                      h2=h2,
                      h3=h3,
                      angle=angle,
                      status=status_code,
                      geo_location=geoLoc,
                      street=street,
                      locality=locality,
                      city=city,
                      state=state,
                      postal_code=postal_code,
                      country=country,
                      operator=operator,
                      auth_code=scan_auth,
                      product_details=productDetails,
                      bit_mask=bit_mask,
                      color_profile=color_profile,
                      image=image,
                      email_id=email_id,
                      company_name=company_name
                      )
    v.save()
    try:
     #print email_id
     send_confirmation(email_id,asset_code,status,scan_time,location,operator,company_name,image)
    except:
     print "email sending failed"
    #syncdata(asset_code,time_millis,credential,status,d1,d2,d3,h1,h2,h3,angle,orrcredential,color_profile,geoLoc,operator,username,password,scan_auth,productDetails,bit_mask,email_id)
    
