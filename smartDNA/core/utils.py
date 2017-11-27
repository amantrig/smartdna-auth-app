import os
import sys
import xlwt
import datetime
import os
import zipfile
import tempfile
import shutil
import time
from pysimplesoap.client import SoapClient
from django.forms.forms import pretty_name
from django.core.exceptions import ObjectDoesNotExist
from cStringIO import StringIO
from django.core.files.base import ContentFile
from django.shortcuts import HttpResponse
from os.path import basename
from PIL import Image
from django.core.mail import get_connection,send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
import urllib
from urllib2 import urlopen, Request

os.environ['PYTHON_EGG_CACHE'] = "/tmp"

PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH+'smartDNA/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'
from django.conf import settings
from django.contrib.gis.geoip import GeoIP

WORK_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]+'smartDNA/'

HEADER_STYLE = xlwt.easyxf('font: bold on')
DEFAULT_STYLE = xlwt.easyxf()
CELL_STYLE_MAP = (
    (datetime.date, xlwt.easyxf(num_format_str='DD/MM/YYYY h:mm AM/PM')),
    (datetime.time, xlwt.easyxf(num_format_str='HH:MM')),
    (bool,          xlwt.easyxf(num_format_str='BOOLEAN')),
)

STATUS_CHOICES=(
    (1,'Registered'),
    (2,'Verified'),
    (3,'Tampered'),
    (4,'Tampered with line cut'),
    (5,'Discrepant Label'),
    (6,'Void'),
    (7,'Barcode Error'),
    (8,'Label Error'),
    (9,'Height Error'),
    (10,'Released'),
    (11,'Audited'),
    (12, 'Unregistered'),
    (13,'Verified-x'),
    (14,'Tampered-2'),
    (15,'Tampered-3'),
    )

def sendSMS(user, senderID, receipientno, msgtxt):
    data =  urllib.urlencode({'user':user,'senderID': senderID, 'receipientno': receipientno,'msgtxt' : msgtxt})
    data = data.encode('utf-8')
    print data
    request = Request('http://api.mvaayoo.com/mvaayooapi/MessageCompose?')
    f = urlopen(request, data)
    fr = f.read()
    return(fr)

def getAddress(geo_location):
  location ={'street':'none','locality':'none','city':'none','state':'none','postal_code':'none','country':'none'}
  try:
   from pygeocoder import Geocoder
   #print "try reverse geo-coding"
   g1,g2=geo_location.split('|')
   result= Geocoder.reverse_geocode(float(g1), float(g2))
   #print result
   location['street']=(str(result.street_number)+', '+str(result.route))[:64]
   location['locality']=(str(result.sublocality_level_3)+', '+str(result.sublocality_level_2)+', '+str(result.sublocality_level_1)+', '+str(result.locality))[:128]
   location['city']=str(result.administrative_area_level_2)
   location['state']=str(result.administrative_area_level_1)
   location['postal_code']=str(result.postal_code)
   location['country']=str(result.country)
  except:
   print "failed reverse geo-coding"
  return location

def getStatusCode(status):
  status_code=''
  for choice in STATUS_CHOICES:
    if status==choice[1]:
      status_code=choice[0]
      break
  return status_code


def get_email_connection():
    from core.models import Configuration
    config = Configuration.objects.filter(dep_name=1)[0]
    use_tls = True
    use_ssl = False
    fail_silently=False
    connection = get_connection(host=config.email_host, 
                            port=config.email_port, 
                            username=config.email_user, 
                            password=config.email_pass, 
                            use_tls=use_tls,
                            use_ssl=use_ssl,
			    fail_silently=fail_silently)
    return connection 

def trim_tuple(original_tuple, element_to_remove):
    new_tuple = []
    for s in list(original_tuple):
        if not s == element_to_remove:
            new_tuple.append(s)
    return tuple(new_tuple)

def get_ip(request):
   xff = request.META.get('HTTP_X_FORWARDED_FOR')
   if xff:
      return xff.split(',')[0]
   return request.META.get('REMOTE_ADDR')

def get_address(request):
   ip = get_ip(request)
   g = GeoIP()
   c = g.city(ip)
   return c

def zip_file(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()

def zip_file2(src, stream):
    zf = zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()
    shutil.rmtree(src)

def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj

def get_column_head(obj, name):
    name = name.rsplit('.', 1)[-1]
    return pretty_name(name)

def get_column_cell(obj, name):
    try:
        attr = multi_getattr(obj, name)
    except ObjectDoesNotExist:
        return None
    if hasattr(attr, '_meta'):
        # A Django Model (related object)
        return unicode(attr).strip()
    elif hasattr(attr, 'all'):
        # A Django queryset (ManyRelatedManager)
        return ', '.join(unicode(x).strip() for x in attr.all())
    return attr

def queryset_to_workbook(queryset, columns, header_style=None,
                         default_style=None, cell_style_map=None):
    workbook = xlwt.Workbook()
    report_date = datetime.date.today()
    sheet_name = 'Export {0}'.format(report_date.strftime('%Y-%m-%d'))
    sheet = workbook.add_sheet(sheet_name)

    if not header_style:
        header_style = HEADER_STYLE
    if not default_style:
        default_style = DEFAULT_STYLE
    if not cell_style_map:
        cell_style_map = CELL_STYLE_MAP

    obj = queryset[0]
    for y, column in enumerate(columns):
        value = get_column_head(obj, column)
        sheet.write(0, y, value, header_style)

    for x, obj in enumerate(queryset, start=1):
        for y, column in enumerate(columns):
            #print column
	    if str(column) == "image":
	     value =str(getattr(obj, "image"))
	    elif str(column) == "status":
             #print STATUS_CHOICES[getattr(obj, "status")-1][1]
	     value = str(STATUS_CHOICES[getattr(obj, "status")-1][1])
	    else:
             value = get_column_cell(obj, column)
            #print value
            style = default_style
            for value_type, cell_style in cell_style_map:
                if isinstance(value, value_type):
                    style = cell_style
            sheet.write(x, y, value, style)

    return workbook

def queryset_to_mediabook(queryset):
    directory=WORK_PATH+"media/documents/export_media_"+str(time.time())
    if not os.path.exists(directory):
    	os.makedirs(directory)
    for obj in queryset:
	d1,d2,d3,file_name=str(obj.image).split('/')
	#print file_name
	#os.chmod(WORK_PATH+"media/documents/"+file_name,0777)
	if os.path.isfile(WORK_PATH+"media/documents/"+file_name):
	 shutil.copyfile(WORK_PATH+"media/documents/"+file_name,directory+"/"+file_name)
    zip_file(directory+"/",directory)
    return directory+".zip"

def export_media2(queryset,username):
    stream = StringIO()
    directory=WORK_PATH+"media/documents/exported_media_files_"+username+"_"+str(time.time())
    if not os.path.exists(directory):
    	os.makedirs(directory)
    for obj in queryset:
	d1,d2,d3,file_name=str(obj.image).split('/')
	if os.path.isfile(WORK_PATH+"media/documents/"+file_name):
	 shutil.copyfile(WORK_PATH+"media/documents/"+file_name,directory+"/"+file_name)
    zip_file2(directory+"/",stream,)
    response = HttpResponse(stream.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment;'+ 'filename="'+'exported_media_files_'+username+'_'+str(time.time())+'.zip"'
    return response

def export_media(queryset):
    directory=WORK_PATH+"media/documents/"
    stream = StringIO()
    temp_zip_file = zipfile.ZipFile(stream, 'w')
    for obj in queryset:
     if os.path.isfile(WORK_PATH+str(obj.image)):
      temp_zip_file.write(WORK_PATH+str(obj.image),directory)

    temp_zip_file.close()
    response = HttpResponse(stream.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="media_files.zip"'
    return response

#Ask any client to create same kind of API where just URL changes and create a URL_CONF.JOSN. Store all
#the URLs in ther and just parse in in the post_data_remote_serever method.
def post_data_2sv(asset_code,time_millis,credential,status,operator,geo_location,location,mobile_number,image,atm_id,bit_mask):
    scan_time=datetime.datetime.fromtimestamp(float(time_millis)/1e3).strftime('%m/%d/%Y %H:%M:%S')
    #print scan_time, type(scan_time)
    try:
     client = SoapClient(wsdl="http://221.135.139.45:8112/LinkSmartWS.asmx?WSDL",trace=False,)
     response = client.ScanData(asset_code=asset_code,scan_time=scan_time,credential=credential,status=status,Operator=operator,geo_location=geo_location,location=location,mobile_number=mobile_number,image=image,atm_id=atm_id,bit_mask=bit_mask)
     #print response
     result = response['ScanDataResult']['Remark']
     print result
    except:
     result = "server error"
     print result

def compress_image(imagefile):
    response=False
    try:
     filename, file_extension = os.path.splitext(imagefile)
     print basename(filename)
     im = Image.open(imagefile)
     im.convert('RGB').save(filename+".jpg", 'JPEG')
     #bg = Image.new("RGBA", im.size, (255,255,255))
     #bg.paste(im,(0,0),im) #OR
     #bg = Image.new("RGB", im.size, (255,255,255))
     #bg.paste(im,im)
     #bg.save(filename+".jpg")#,quality=50)
     #print "image file size "+str(len((StringIO(open(filename+".jpg",'rb').read()).read())))
     response=True
    except:
     response=False
    print "compression result: "+str(response)
    return response

def user_details(subject,username,password):
  yield '<div style="background-color:#eaeef0;width:100%;height:100%;">'
  yield '<table style="width:460px;background-color:white;margin: 0 auto;">'
  yield '<tr><td></td><td><h4>%s</h4></td><td></td></tr>'%(subject)
  yield '<tr><td></td><td>%s</td><td></td></tr>'%('---------------------------------------------------------------------------------------------------')
  yield '<tr><td></td><td><strong>%s</strong>%s</td><td></td></tr>'%('Username: ',username)
  yield '<tr><td></td><td><strong>%s</strong>%s</td><td></td></tr>'%('Password: ',password)
  yield '<tr><td></td><td>%s</td><td></td></tr>'%('---------------------------------------------------------------------------------------------------')
  yield '<tr><td></td><td>%s</td><td></td><tr>'%('Please contact your company admin for sAMM in case you have any question regarding this.')
  yield '</table>'
  yield '</div>'

def mail_template_generator(subject,details):
  #print details
  yield '<div style="background-color:#eaeef0;width:100%;height:100%;">'
  yield '<div style="width:460px;background-color:white;margin: 0 auto;">'
  yield '<h4 style="padding-left:1.5em;padding-right:1.5em;padding-top:0.5em;">%s</h4>'%(subject)
  yield '<table style="padding-left:1.5em;padding-right:1.5em;">'
  for key in details:
    yield '<tr><td>%s</td><td>%s</td></tr>'%(key,details[key])
  yield '</table>'
  yield '<p style="padding:1.5em;color:#3333ff;"> This is an automatically generated email, please <strong>do not reply.</strong></p>'
  yield '</br>'
  yield '</div>'
  yield '</div>'

def send_confirmation(email_id,asset_code,status,scan_time,location,operator,company_name,image):
    from collections import OrderedDict
    connection=get_email_connection()
    details = OrderedDict([('Asset ID:',asset_code),
    	('Status:',status),
    	('Time of Scan:',scan_time),
    	('Location of Scan:',location),
    	('Scanned by:',operator),
    	('Company Name:',company_name),])
    subject="Product authentication details:"
    text_content = "Product authentication details:"
    html_content = "".join(mail_template_generator(subject,details))
    #print html_content,PROJECT_PATH+"smartDNA"+image
    msg = EmailMultiAlternatives("smartDNA authentication- "+company_name+" - "+asset_code, text_content, settings.EMAIL_HOST_USER,[email_id],connection=connection)
    msg.attach_alternative(html_content, "text/html")
    try:
     if(image.split("/")[-1] != "signature-not-found-4.png"):
      fp = open(PROJECT_PATH+"smartDNA"+image, 'rb')
      msg_img = MIMEImage(fp.read())
      fp.close()
      msg_img.add_header('Content-ID', '<{}>'.format(fp))
      msg.attach(msg_img)
    except:
     print "send_confirmation,no image found!"
    msg.send()


def alert_tm(asset_code,status,scan_time,location,operator,company_name,dep_path,get_model):
    from collections import OrderedDict
    AlertSubscriber= get_model(dep_path, 'AlertSubscriber')
    Alert= get_model(dep_path, 'Alert')
    scr_list= [scr.email for scr in AlertSubscriber.objects.filter(scr_status="Active")]
    #print "subscriber list ",scr_list
    details = OrderedDict([('Asset ID:',asset_code),
    	('Status:',status),
    	('Time of Scan:',scan_time),
    	('Location of Scan:',location),
    	('Scanned by:',operator),
    	('Company Name:',company_name),])
    heading_text="Asset Scan Alert"
    html_content = "".join(mail_template_generator(heading_text,details))
    a=Alert(tracking_code=asset_code,alert_message=status)
    a.save()
    connection=get_email_connection()
    try:
     msg = EmailMultiAlternatives("smartDNA product authentication alert- "+company_name,heading_text, settings.EMAIL_HOST_USER,scr_list,connection=connection)
     msg.attach_alternative(html_content, "text/html")
     msg.content_subtype = "html"
     msg.send()
    except:
     print "alert sending failed"

def email_password(email_id,username,password):
    connection=get_email_connection()
    subject="Your new login details of sAMM account are mentioned below: "
    text_content = " "
    html_content = "".join(user_details(subject,username,password))
    try:
      msg = EmailMultiAlternatives("sAMM account details", text_content, settings.EMAIL_HOST_USER,[email_id],connection=connection)
      msg.attach_alternative(html_content, "text/html")
      msg.send()
    except:
      print "password mailing failed"