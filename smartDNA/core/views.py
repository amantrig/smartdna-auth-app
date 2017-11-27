from django.contrib.auth import authenticate
from django.shortcuts import render_to_response,HttpResponse,HttpResponseRedirect
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from core.forms import AnomalyForm,LoginForm, CheckForm,TrackTraceCheckForm,FetchForm,ScanAnalysisForm,DateRangeForm,BatchReportForm,SettingsForm,UpdateProductDetailsForm
from core.models import Deployment
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.model_utils import identify_noise,tamp_state
from core.utils import queryset_to_mediabook,export_media,export_media2,post_data_2sv,compress_image,getStatusCode,getAddress,sendSMS
from os.path import basename
import os
import datetime
import json
import time
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]

#This API is used by mobile client to login into application
@csrf_exempt
def login(request):
  if request.method == "POST":
    form = LoginForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      usrname = form.cleaned_data['username']
      passwd = form.cleaned_data['password']
      user = authenticate(username=usrname, password=passwd)
      dep=Deployment.objects.filter(user=user)
      if user is not None:
          user_type=dep[0].user_type
          if user.is_superuser:
              data="admin"
          elif user_type=="Operator":
              data="operator"
	  elif user_type=="Vendor":
	      data="vendor"
          else:
              data= "auditor"
      else:
          data= "Invalid User"
    else:
        data= "Missing Data"
  else:
    data="Invalid Request"

  return render_to_response('raw.html', {
        'data': data,
    })

@csrf_exempt
def json_register(request):
    data=""
    model_name='Verification'
    if request.method == "POST":
     username=request.POST['username']
     password=request.POST['password']
     auth_code=request.POST['scan_auth']
     scanner_mode=request.POST['scanner_mode']
     json_file = request.FILES['json_file']
     user = authenticate(username=username, password=password)
     if user is not None:
      #print user
      inconsistent=False
      alreadyReg=False
      dep=Deployment.objects.filter(user=user)
      dep_path=dep[0].dep_path
      from django.db.models.loading import get_model
      json_data = json.load(json_file)
      geo_location=json_data[0]['location']
      location="not found"
      if scanner_mode!="regular":
         location=getAddress(geo_location)
         model_name="Registration"
      Verification = get_model(dep_path, model_name)
      obj_list = []
      for records in json_data:
       #print records
       time_millis=records['time_millis']
       asset_code=records['asset_code']
       operator=records['operator']
       bit_mask=records['bit_mask']
       product_details=records['productDetails']
       status=records['status']
       company_name=records['company_name']
       img_link="/media/documents/signature-not-found-4.png"
       #parsing bit_mask
       bm=[]
       try:
        bm=bit_mask.split('|')
        #print bm
       except:
        print "bit mask parsing error"

       #Parsing address from geo-point
       if scanner_mode=="regular":
        geo_location=records['location']
        location=getAddress(geo_location)
        print "scanner mode- regular"

       if len(bm)>7 and bm[5]=='true':
        img_link='/media/documents/'+asset_code+"_"+operator+"_"+time_millis+".jpg"

       status_code=getStatusCode(status)
       scan_time=datetime.datetime.fromtimestamp(float(time_millis)/1e3).strftime('%Y-%m-%d %H:%M:%S')
       #print scan_time
       records['scan_time'] = scan_time
       records['status'] = status_code
       records['geo_location'] = geo_location
       records['street'] = location['street']
       records['locality'] = location['locality']
       records['city'] = location['city']
       records['state'] = location['state']
       records['postal_code'] = location['postal_code']
       records['country'] = location['country']
       records['auth_code'] = auth_code
       records['product_details']=product_details
       records['image'] = img_link
       del records['time_millis']
       del records['username']
       del records['password']
       del records['productDetails']
       try:
        regCount=0
        if status_code==1:
           regCount=Verification.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name).count()
        if status_code==1 and regCount>0:
         alreadyReg=True
        else:
         v=Verification(**records)
         obj_list.append(v)
         data="Success"
       except:
        inconsistent=True
       if alreadyReg:
        data="Success-P1"
       if inconsistent:
        data="Success-P2"
      try:
       print "Bulk create running.."
       Verification.objects.bulk_create(obj_list,batch_size=10000)
      except:
       print "Bulk Upload Failed"
       data="upload failed"
     else:
      data="unauthorised access"
    else:
     data="Invalid Request"
    return render_to_response('raw.html', {
        'data': data,
  })

@csrf_exempt
def fetch_track_trace(request):
    data=""
    if request.method == "POST":
       form = FetchForm(request.POST) # A form bound to the POST data
       if form.is_valid(): # All validation rules pass
          username = form.cleaned_data['username']
          password = form.cleaned_data['password']
          asset_code = form.cleaned_data['asset_code']
          company_name = form.cleaned_data['company_name']
          print asset_code
          user = authenticate(username=username, password=password)
          if user is not None:
             dep=Deployment.objects.filter(user=user)
             dep_path=dep[0].dep_path
             #Check whether asset code is under anomaly condition or
             from django.utils.importlib import import_module
             Anomaly = import_module(dep_path+'.Anomaly')
             from django.db.models.loading import get_model
             Verification = get_model(dep_path, 'Verification')
             Registration = get_model(dep_path, 'Registration')
             print dep_path
             if Anomaly.isAnomaly(asset_code):
                data="anomaly"
                print "anomaly",asset_code
             elif Registration.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name).count()>0:
                print "registration",asset_code
                v=Registration.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name)[0]
                q=Verification.objects.filter(asset_code__iexact=asset_code,company_name=company_name)
                vcount=q.exclude(status=1).count()
                data=str(v.track_trace_credential())+'|'+str(vcount)
             elif Verification.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name).count()>0:
                print "verification",asset_code
                v=Verification.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name)[0]
                q=Verification.objects.filter(asset_code__iexact=asset_code,company_name=company_name)
                vcount=q.exclude(status=1).count()
                data=str(v.track_trace_credential())+'|'+str(vcount)
             else:
                data="none"
          else:
            data="unauthorised access"
       else:
        data= ": Missing Data"
    else:
      data="Invalid Request"
    return render_to_response('raw.html', {'data': data,})

@csrf_exempt
def fetch(request):
    data=""
    if request.method == "POST":
        form = FetchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            asset_code = form.cleaned_data['asset_code']
	    company_name = form.cleaned_data['company_name']
            print asset_code
            user = authenticate(username=username, password=password)
            if user is not None:
             dep=Deployment.objects.filter(user=user)
    	     dep_path=dep[0].dep_path
             #Check whether asset code is under anomaly condition or
	     from django.utils.importlib import import_module
	     Anomaly = import_module(dep_path+'.Anomaly')
             from django.db.models.loading import get_model
             Verification = get_model(dep_path, 'Verification')
             Registration = get_model(dep_path, 'Registration')
	     print dep_path
             if Anomaly.isAnomaly(asset_code):
                data="anomaly"
                print "anomaly",asset_code
             elif Registration.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name).count()>0:
                print "registration",asset_code
                v=Registration.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name)[0]
                q=Verification.objects.filter(asset_code__iexact=asset_code,company_name=company_name)
                vcount=q.exclude(status=1).count()
                data=str(v.total_credential())+'|'+str(vcount)
             elif Verification.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name).count()>0:
                print "verification",asset_code
                v=Verification.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name)[0]
                q=Verification.objects.filter(asset_code__iexact=asset_code,company_name=company_name)
                vcount=q.exclude(status=1).count()
                data=str(v.total_credential())+'|'+str(vcount)
             else:
                data="none"
            else:
	       data="unauthorised access"
        else:
            data= ": Missing Data"
    else:
        data="Invalid Request"
    return render_to_response('raw.html', {
        'data': data,
  })

@csrf_exempt
def sms_fetch(request):
    data='none'
    body_unicode = request.body.decode()
    print "body unicode", str(body_unicode)
    #print request.REQUEST
    sender = request.REQUEST['sender']
    comments = request.REQUEST['msg']
    if 'RGTR' in comments:
     print comments
     record=(comments[6:]).split('&')
     print "record first ",record[0]
     print "records length ",len(record)
     asset_code=record[1]
     time_millis=record[2]
     scan_time=datetime.datetime.fromtimestamp(float(time_millis)/1e3).strftime('%Y-%m-%d %H:%M:%S')
     credential=record[3]
     orrcredential='1000'
     d1='0.0'
     d2='0.0'
     d3='0.0'
     h1='0.0'
     h2='0.0'
     h3='0.0'
     angle='888.0'
     status=record[4]
     status_code=getStatusCode(status)
     g1=record[5]
     g2=record[6]
     geoLoc=g1+'|'+g2
     location=getAddress(geoLoc)
     operator='sms_user'
     username='sms_user'
     password=''
     scan_auth=sender
     productDetails=record[8]
     bit_mask=record[7]
     color_profile='nft'
     img_link="/media/documents/signature-not-found-4.png"
     try:
      company_name=record[9]
     except:
      company_name='Pioneer'
     try:
      email_id = record[10]
     except:
      email_id='none'
     bm=[]
     try:
      bm=bit_mask.split('|')
      #print bm
     except:
      print "bit mask parsing error"
     from django.utils.importlib import import_module
     save_data = import_module('smartdna'+'.save_data')
     if len(bm)>6 and bm[5]=='true':
      img_link='/media/documents/'+asset_code+"_"+operator+"_"+time_millis+".jpg"
      #print img_link
     if status_code==1 and Verification.objects.filter(asset_code__iexact=asset_code,status=1).count()>0:
      data='Success'
     else:
      save_data.saveData(asset_code,scan_time,time_millis,credential,int(orrcredential), d1,d2,d3,h1,h2,h3,angle,status,status_code,
          geoLoc,location['street'],location['locality'],location['city'],location['state'],location['postal_code'],location['country'],
          operator,username,password,scan_auth,productDetails,bit_mask,color_profile,img_link,email_id,company_name)
      data='Success'
    else:
     asset_code,company_name = (comments[6:]).split('_')
     print sender,asset_code,company_name
     from django.db.models.loading import get_model
     Verification = get_model('smartdna', 'Verification')
     Registration = get_model('smartdna', 'Registration')
     if Registration.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name).count()>0:
      v=Registration.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name)[0]
      q=Verification.objects.filter(asset_code__iexact=asset_code,company_name=company_name)
      vcount=q.exclude(status=1).count()
      credential=str(v.sms_credential())+'-scan_count='+str(vcount)
      resp=sendSMS('sushil.acharya@empover.com:empover','PHISMS', sender, credential)
      data=resp
     elif Verification.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name).count()>0:
      v=Verification.objects.filter(asset_code__iexact=asset_code,status=1,company_name=company_name)[0]
      q=Verification.objects.filter(asset_code__iexact=asset_code,company_name=company_name)
      vcount=q.exclude(status=1).count()
      credential=str(v.sms_credential())+'-scan_count='+str(vcount)
      resp=sendSMS('sushil.acharya@empover.com:empover','PHISMS', sender, credential)
      data=resp
     else:
      data='none'
      credential='Barcode='+asset_code+'-company_name='+company_name+'-status='+"Unregistered"
      resp=sendSMS('sushil.acharya@empover.com:empover','PHISMS', sender, credential)
      data=resp
    return render_to_response('raw.html', {
        'data': data,
  })

@csrf_exempt
def track_trace_register(request):
    if request.method == "POST":
     form = TrackTraceCheckForm(request.POST)
     if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      auth_code = form.cleaned_data['scan_auth']
      email_id = form.cleaned_data['email_id']
      company_name = form.cleaned_data['company_name']
      scan_records = json.load(request.FILES['scan_records'])
      #print scan_records
      user = authenticate(username=username, password=password)
      if user is not None:
       for records in scan_records:
        #print company_name
        asset_code=records['asset_code']
        time_millis=records['time_millis']
        operator=username
        bit_mask=records['bit_mask']
        status=records['status']
        geo_location=records['location']
        img_link="/media/documents/signature-not-found-4.png"
        #parsing bit_mask
        bm=[]
        try:
         bm=bit_mask.split('|')
        except:
         print "bit mask parsing error"
        location=getAddress(records['location'])
        if len(bm)>7 and bm[5]=='true':
         img_link='/media/documents/'+asset_code+"_"+operator+"_"+time_millis+".jpg"
        status_code=getStatusCode(status)
        scan_time=datetime.datetime.fromtimestamp(float(time_millis)/1e3).strftime('%Y-%m-%d %H:%M:%S')
        records['scan_time'] = scan_time
        records['status'] = status_code
        records['geo_location'] = geo_location
        records['street'] = location['street']
        records['locality'] = location['locality']
        records['city'] = location['city']
        records['state'] = location['state']
        records['postal_code'] = location['postal_code']
        records['country'] = location['country']
        records['operator'] = operator
        records['auth_code'] = auth_code
        records['email_id'] = email_id
        records['company_name'] = company_name
        records['product_details']=records['product_details']
        records['image'] = img_link
        del records['time_millis']
        del records['location']
        dep=Deployment.objects.filter(user=user)
        dep_path=dep[0].dep_path
        from django.db.models.loading import get_model
        Registration = get_model(dep_path, 'Registration')
        try:
         v=Registration(**records)
         v.save()
         data="Success"
        except:
         print "Duplicate asset ids not allowed"
         data="Success-P1"
      else:
       data = "Wrong username or password"
     else:
      data= ": Missing Data"
    else:
     data="Invalid Request"
    return render_to_response('raw.html',{'data': data,})

@csrf_exempt
def register(request):
   username = request.POST['username']
   password = request.POST['password']
   user = authenticate(username=username, password=password)
   if user is not None:
       data ="authorized user"
   else:
      data = "Wrong username or password"
   if data == "Wrong username or password":
     return render_to_response('raw.html', {
                 'data': data,
      })

   if request.method == "POST":
     form = CheckForm(request.POST) # A form bound to the POST data
     if form.is_valid(): # All validation rules pass
       asset_code= str(form.cleaned_data['asset_code'])
       time_millis=str(form.cleaned_data['scan_time'])
       scan_time=datetime.datetime.fromtimestamp(float(time_millis)/1e3).strftime('%Y-%m-%d %H:%M:%S')
       credential= str(form.cleaned_data['credential'])
       orrcredential= str(form.cleaned_data['orrcredential'])
       d1= form.cleaned_data['d1']
       d2= form.cleaned_data['d2']
       d3= form.cleaned_data['d3']
       h1= form.cleaned_data['h1']
       h2= form.cleaned_data['h2']
       h3= form.cleaned_data['h3']
       angle = form.cleaned_data['angle']
       status= str(form.cleaned_data['status'])
       operator= str(form.cleaned_data['operator'])
       geoLoc= str(form.cleaned_data['location'])
       scan_auth= str(form.cleaned_data['scan_auth'])
       productDetails= str(request.POST['productDetails'])
       bit_mask =str(form.cleaned_data['bit_mask'])
       company_name=str(form.cleaned_data['company_name'])
       color_profile =str(form.cleaned_data['color_profile'])
       img_link="/media/documents/signature-not-found-4.png"
       email_id = str(form.cleaned_data['email_id'])
       #parsing bit_mask
       bm=[]
       try:
        bm=bit_mask.split('|')
        #print bm
       except:
        print "bit mask parsing error"
       #parsing address from geo-codes.
       location=getAddress(geoLoc)
       model_name='Verification'
       dep=Deployment.objects.filter(user=user)
       dep_path=dep[0].dep_path
       from django.db.models.loading import get_model
       from django.utils.importlib import import_module
       from core.utils import alert_tm
       if status=='Registered':
        model_name='Registration'
       Verification = get_model(dep_path, model_name)

       status_code=getStatusCode(status)
       if status_code in (3,4,5,8,12):
        alert_tm(asset_code,status,scan_time,location,operator,company_name,dep_path,get_model)
       #print dep_path
       save_data = import_module(dep_path+'.save_data')
       if len(bm)>6 and bm[5]=='true':
        img_link='/media/documents/'+asset_code+"_"+operator+"_"+time_millis+".jpg"
       #print img_link
       if status_code==1 and Verification.objects.filter(asset_code__iexact=asset_code,status=1).count()>0:
        data="Success"
       else:
        save_data.saveData(asset_code,scan_time,time_millis,credential,int(orrcredential), d1,d2,d3,h1,h2,h3,angle,status,status_code,
          geoLoc,location['street'],location['locality'],location['city'],location['state'],location['postal_code'],location['country'],
          operator,username,password,scan_auth,productDetails,bit_mask,color_profile,img_link,email_id,company_name)
        data="Success"
     else:
         data= ": Missing Data"
   else:
     data="Invalid Request"

   return render_to_response('raw.html', {
         'data': data,
   })

def monitoring(request):
    return render_to_response('monitoring.html',context_instance=RequestContext(request))

def get_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def get_port(request):
    if 'SERVER_PORT' in request.META:
        return request.META['SERVER_PORT']
    else:
        return None

def live_chart_data(request):
    #from django.db.models import Count
    dep = Deployment.objects.filter(user=request.user)
    dep_path = dep[0].dep_path
    from django.db.models.loading import get_model
    try:
     Verification = get_model(dep_path, 'Verification')
     verification=Verification.objects.filter(status__in=['1','2','3','5','8','10'])
     rRows = verification.filter(status=1).count()
     vRows = verification.filter(status=2).count()
     tRows = verification.filter(status=3).count()
     dRows = verification.filter(status=5).count()
     eRows = verification.filter(status=8).count()
     aRows = verification.filter(status=10).count()
     #Verification.objects.values('status').annotate(dcount=Count('status'))
     raw_string='{"cols": [{"id":"","label":"Topping","pattern":"","type":"string"},{"id":"","label":"Slices","pattern":"","type":"number"}],"rows": [{"c":[{"v":"Registered","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Tampered","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Discrepant","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Verified","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Label Error","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Released","f":null},{"v":%s,"f":null}]}]}' % (rRows,tRows,dRows,vRows,eRows,aRows)
     return HttpResponse(raw_string, content_type="application/json")
    except:
     return HttpResponse('none', content_type="application/json")

def dashboard(request):
    from django.db.models.loading import get_model,get_app,get_models
    try:
     dep = Deployment.objects.filter(user=request.user)
     dep_path = dep[0].dep_path
     Verification = get_model(dep_path, 'Verification')
     ActivityLog = get_model(dep_path, 'ActivityLog')
     from core.models import Logger
     activity_data=ActivityLog.objects.all().order_by("-activity_time")[:10]
     last_login = Logger.objects.all().order_by("-login_time")[0]
     return render_to_response('admin/dashboard.html',{'last_login':last_login,'activity_data':activity_data},
	context_instance=RequestContext(request))
    except:
     return HttpResponseRedirect("/admin/")

@csrf_exempt
def upload_image(request):
    print "image file"
    if request.method == 'POST':
       print "posted"
       username=request.POST['username']
       password=request.POST['password']
       myfile = request.FILES['myfile']
       filename = myfile.name
       print filename,username,password
       user = authenticate(username=username, password=password)
       if user is not None:
        fd = open(PROJECT_PATH+'smartDNA/media/documents/'+filename, 'wb+',00777)
        print "open file object"
        for chunk in myfile.chunks():
            fd.write(chunk)
        fd.close()
        print filename,"Uploaded Successfully"
        return HttpResponse("OK")
       else:
	return HttpResponse("Invalid User")
    else:
       return HttpResponse("Not Ok")

@csrf_exempt
def upload_postmortem_image(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        myfile = request.FILES['myfile']
        filename =myfile.name
        print filename,username,password
        user = authenticate(username=username, password=password)
        if user is not None:
         asset_code,username,time_millis,ctwext=filename.split('|')
         case_type,ext=ctwext.split('.')
	 scan_time=datetime.datetime.fromtimestamp(float(time_millis)/1e3).strftime('%Y-%m-%d %H:%M:%S')
         fd = open(PROJECT_PATH+'smartDNA/media/postmortem_image/' + filename,'wb+',00777)
         imagefile='/media/postmortem_image/'+filename
         print imagefile
	 dep=Deployment.objects.filter(user=user)
    	 dep_path=dep[0].dep_path
         from django.db.models.loading import get_model
    	 PostmortemImage = get_model(dep_path, 'PostmortemImage')
         imdoc=PostmortemImage(asset_code=asset_code,scan_time=scan_time,case_type=case_type,imagefile=imagefile)
         imdoc.save()
         for chunk in myfile.chunks():
             fd.write(chunk)
         fd.close()
         print "upload success!"
         return HttpResponse("OK")
        else:
         return HttpResponse("Invalid User")
    else:
        return HttpResponse("Not Ok")

@csrf_exempt
def anomalyReg(request):
    print "Trying to post anomaly"
    if request.method == "POST":
        print "Anomaly posted"
        form = AnomalyForm(request.POST) # A form bound to the POST data
        if form.is_valid():# All validation rules pass
            print "Anomaly valid post"
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            asset_code= form.cleaned_data['asset_code']
	    scan_time=str(datetime.datetime.now())
            operator= form.cleaned_data['operator']
	    location= form.cleaned_data['location']
            print asset_code,operator
            ostatus=""
            user = authenticate(username=username, password=password)
            if user is not None:
       	        dep=Deployment.objects.filter(user=user)
    		dep_path=dep[0].dep_path
             	from django.db.models.loading import get_model
    		Anomaly = get_model(dep_path, 'Anomaly')
       	        anomaly=Anomaly(asset_code=asset_code,scan_time=scan_time,operator=operator,location=location)
		anomaly.save()
                data="Success"
            else:
                data="Wrong username or password"
        else:
            data= ": Missing Data"
    else:
        data="Invalid Request"
    return render_to_response('raw.html', {'data': data,})

def support(request):
    with open(PROJECT_PATH+'smartDNA/media/patrol-monitoring-application-guide.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=patrol-monitoring-application-guide.pdf'
        return response
    pdf.closed

def analytics(request):
   data="Feature on Demand"
   return render_to_response('admin/analytics.html', {'data': data,})

def audit_monitoring(request):
    username=request.user
    dep=Deployment.objects.filter(user=username)
    dep_path=dep[0].dep_path
    url_path="/admin/"+dep_path+"/verification/"
    return HttpResponseRedirect(url_path)

def registration_monitoring(request):
    username=request.user
    dep=Deployment.objects.filter(user=username)
    dep_path=dep[0].dep_path
    url_path="/admin/"+dep_path+"/registration/"
    return HttpResponseRedirect(url_path)

def cmonitoring(request):
    username=request.user
    dep=Deployment.objects.filter(user=username)
    dep_path=dep[0].dep_path
    from django.db.models.loading import get_model
    Verification = get_model(dep_path, 'Verification')
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
         d1 = form.cleaned_data['day1']
         d2 = (form.cleaned_data['day2']+datetime.timedelta(days=1))
         #store = form.cleaned_data['Store']
         if d1<d2:
          nosort="Remove Filter"
          vdata=Verification.objects.filter(scan_time__range=(d1,d2)).order_by('-scan_time')
          c = str(vdata.count())
          paginator = Paginator(vdata,20 )
          page = request.GET.get('page')
          try:
            data = paginator.page(page)
          except PageNotAnInteger:
            data = paginator.page(1)
          except EmptyPage:
            data = paginator.page(paginator.num_pages)
          total_records ="Total records: "+c
          return render_to_response('admin/cmonitoring.html', {'data': data,'form':form,'pdata':vdata,'nosort':nosort,"total_records":total_records},context_instance=RequestContext(request))
         else:
	     vdata=Verification.objects.all().order_by('-scan_time')
	     c = str(vdata.count())
	     paginator = Paginator(vdata,20 )
	     page = request.GET.get('page')
	     try:
	       data = paginator.page(page)
	     except PageNotAnInteger:
	       data = paginator.page(1)
	     except EmptyPage:
	       data = paginator.page(paginator.num_pages)
	     total_records ="Total records: "+c
             nosort="Remove Filter"
             wrange="Incorrect date range-no filter applied"
             return render_to_response('admin/cmonitoring.html', {'data': data,'pdata':vdata,'form':form,'wrange':wrange,'nosort':nosort,"total_records":total_records},context_instance=RequestContext(request))
        else:
	    vdata=Verification.objects.all().order_by('-scan_time')
            c = str(vdata.count())
            paginator = Paginator(vdata,20 )
            page = request.GET.get('page')
            try:
              data = paginator.page(page)
            except PageNotAnInteger:
              data = paginator.page(1)
            except EmptyPage:
              data = paginator.page(paginator.num_pages)
            total_records ="Total records: "+c
	    nosort="Remove Filter"
            error_message="Invalid date-no filter applied"
            form = DateRangeForm()
            return render_to_response('admin/cmonitoring.html', {'data': data,'pdata':vdata,'error_message': error_message,'form':form,'nosort':nosort,"total_records":total_records},context_instance=RequestContext(request))
    else:
        vdata = Verification.objects.all().order_by('-scan_time')
	c = str(vdata.count())
	total_records ="Total records: "+c
        paginator = Paginator(vdata, 20)
        page = request.GET.get('page')
        form = DateRangeForm()
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        return render_to_response('admin/cmonitoring.html', {
            'data': data,'pdata':vdata,'form':form,"total_records":total_records
            },
            context_instance=RequestContext(request))


def scanmonitoring(request):
    username=request.user
    dep=Deployment.objects.filter(user=username)
    dep_path=dep[0].dep_path
    print dep_path
    from django.db.models.loading import get_model
    from django.db import connection
    cursor = connection.cursor()
    Verification = get_model(dep_path, 'Verification')
    d1 = datetime.date.today()-datetime.timedelta(days=30)
    d2 = datetime.date.today()+datetime.timedelta(days=1)
    cursor.execute('''select asset_code, ver_count from (select asset_code, count(asset_code) as ver_count from smartdna_verification where status != 1 group by asset_code) sq where sq.ver_count >10''')
    assets=cursor.fetchall()
    #asset_list=[]
    pdata=[]
    for p in assets:
      #asset_list.append(p[0])
      try:
        v=Verification.objects.filter(asset_code=p[0],scan_time__range=(d1,d2)).exclude(status=1).order_by('-scan_time')[0]
        pdata.append(v)
      except:
        print 'no records in selected criteria'
    if request.method == 'POST':
        form = ScanAnalysisForm(request.POST)
        if form.is_valid():
         d1 = form.cleaned_data['day1']
         d2 = (form.cleaned_data['day2']+datetime.timedelta(days=1))
         scan_count =str(form.cleaned_data['scan_count'])
         #store = form.cleaned_data['Store']
         if d1<d2:
          cursor.execute('''select asset_code, ver_count from (select asset_code, count(asset_code) as ver_count from smartdna_verification where status != 1 group by asset_code) sq where sq.ver_count >%s'''%(scan_count))
          assets=cursor.fetchall()
          #asset_list=[]
          pdata=[]
          for p in assets:
           #asset_list.append(p[0])
           try:
            v=Verification.objects.filter(asset_code=p[0],scan_time__range=(d1,d2)).exclude(status=1).order_by('-scan_time')[0]
            pdata.append(v)
           except:
            print 'no records in selected criteria'
          #print pdata
          paginator = Paginator(pdata,50)
          page = request.GET.get('page')
          try:
            data = paginator.page(page)
          except PageNotAnInteger:
            data = paginator.page(1)
          except EmptyPage:
            data = paginator.page(paginator.num_pages)
          total_records =str(len(pdata))
          return render_to_response('admin/scanmonitoring.html', {'data': data,'form':form,'pdata':pdata,'total_records':total_records},context_instance=RequestContext(request))
         else:
             total_records =str(len(pdata))
             wrange="Incorrect date range "
             return render_to_response('admin/scanmonitoring.html', {'pdata':pdata,'form':form,'wrange':wrange,'total_records':total_records},context_instance=RequestContext(request))
        else:
            error_message="Invalid date entered"
            total_records =str(len(pdata))
            form = ScanAnalysisForm()
            return render_to_response('admin/scanmonitoring.html', {'pdata':pdata,'error_message': error_message,'form':form,'total_records':total_records},context_instance=RequestContext(request))
    else:
      d1 = datetime.date.today()-datetime.timedelta(days=30)
      d2 = datetime.date.today()+datetime.timedelta(days=1)
      cursor.execute('''select asset_code, ver_count from (select asset_code, count(asset_code) as ver_count from smartdna_verification where status != 1 group by asset_code) sq where sq.ver_count >10''')
      assets=cursor.fetchall()
      #asset_list=[]
      pdata=[]
      for p in assets:
       #asset_list.append(p[0])
       try:
        v=Verification.objects.filter(asset_code=p[0],scan_time__range=(d1,d2)).exclude(status=1).order_by('-scan_time')[0]
        pdata.append(v)
       except:
        print 'no records in selected criteria'
      paginator = Paginator(pdata, 50)
      page = request.GET.get('page')
      form = ScanAnalysisForm()
      try:
        data = paginator.page(page)
      except PageNotAnInteger:
        data = paginator.page(1)
      except EmptyPage:
        data = paginator.page(paginator.num_pages)
      total_records =str(len(pdata))
      return render_to_response('admin/scanmonitoring.html', {
        'data': data,'pdata':pdata,'form':form,'total_records':total_records},context_instance=RequestContext(request))

def asset_status(request,code):
    username=request.user
    dep=Deployment.objects.filter(user=username)
    dep_path=dep[0].dep_path
    print dep_path
    from django.db.models.loading import get_model
    Verification = get_model(dep_path, 'Verification')
    data=Verification.objects.filter(asset_code__iexact=code).order_by('-scan_time')
    asset_code=code
    total_records=str(data.count())#+" records"
    return render_to_response('admin/asset_status.html', {'data': data,'asset_code':asset_code,'total_records':total_records},context_instance=RequestContext(request))

def orr_status(request,asset_code):
	 username=request.user
    	 dep=Deployment.objects.filter(user=user)
     	 dep_path=dep[0].dep_path
    	 print dep_path
     	 from django.db.models.loading import get_model
    	 OrrVerification = get_model(dep_path, 'OrrVerification')
         pdata=OrrVerification.objects.filter(asset_code=asset_code,image_type="Audit").order_by('-id')
	 vdata=OrrVerification.objects.filter(asset_code=asset_code,image_type="Audit").order_by('-id')
	 c = str(vdata.count())
	 nosort="Remove Filter"
	 error_message=""
         if vdata.count()<1:
	  error_message="NO Reocrds Found!"
    	 total_records ="Total Records: "+c
    	 paginator = Paginator(vdata, 24)
    	 page = request.GET.get('page')
    	 try:
       	  data = paginator.page(page)
    	 except PageNotAnInteger:
       	  data = paginator.page(1)
    	 except EmptyPage:
          data = paginator.page(paginator.num_pages)
    	 return render_to_response('admin/orr_status.html', {'data': data,'pdata':pdata,'error_message': error_message,'nosort':nosort,'total_records':total_records},context_instance=RequestContext(request))

def batch_report(request):
    username=request.user
    dep=Deployment.objects.filter(user=username)
    dep_path=dep[0].dep_path
    from django.db.models.loading import get_model
    Verification = get_model(dep_path, 'Verification')
    if request.method == 'POST':
     message=""
     form = BatchReportForm(request.POST)
     if form.is_valid():
      try:
       prefix=str(form.cleaned_data['batch_prefix'])
       start=str(form.cleaned_data['first_batch_id'])
       end=str(form.cleaned_data['last_batch_id'])
       start_date=form.cleaned_data['start_date']
       end_date=(form.cleaned_data['end_date']+datetime.timedelta(days=1))
       status=form.cleaned_data['status']
       action=form.cleaned_data['action']
       if int(status)==1:
        Verification=get_model(dep_path, 'Registration')
       import xlwt
       book = xlwt.Workbook()
       sheet1 = book.add_sheet('sheet1')
       if start_date<end_date:
	if len(start)==len(end):
         if (int(end)>int(start)):
          data=[]
          i=0
          for ids in range(int(start),int(end)+1):
           asset_id=str(ids).zfill(len(str(start)))
           print "asset id ",asset_id
           if Verification.objects.filter(asset_code=prefix+asset_id,status=status,scan_time__range=(start_date,end_date)).exists():
            print "found regisered"
           else:
            sheet1.write(i,0,prefix+asset_id)
	    data.append(prefix+asset_id)
            i=i+1
          if i>0:
           if action=="View":
	    return render_to_response('admin/batch_report.html',{'form':form,'message':message,'data':data,},context_instance=RequestContext(request))
           else:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=missing-ids.xls'
            book.save(response)
            return response
          else:
           uptodate_message="Complete batch exist in database under provided filter"
           form = BatchReportForm()
           return render_to_response('admin/batch_report.html',{'form':form,'uptodate_message':uptodate_message,},context_instance=RequestContext(request))
         else:
          message="Batch End ID should be greater than Batch Start ID"
          form = BatchReportForm()
          return render_to_response('admin/batch_report.html',{'form':form,'message':message,},context_instance=RequestContext(request))
	else:
         message="Invalid batch entered"
         form = BatchReportForm()
         return render_to_response('admin/batch_report.html',{'form':form,'message':message,},context_instance=RequestContext(request))
       else:
        message="To date should be greater than or equal to From date"
        form = BatchReportForm()
        return render_to_response('admin/batch_report.html',{'form':form,'message':message,},context_instance=RequestContext(request))
      except ValueError:
       message="Invalid Entry"
       form = BatchReportForm()
       return render_to_response('admin/batch_report.html',{'form':form,'message':message,},context_instance=RequestContext(request))
     else:
      message="Invalid Entry"
      form = BatchReportForm()
      return render_to_response('admin/batch_report.html',{'form':form,'message':message,},context_instance=RequestContext(request))
    else:
     form = BatchReportForm()
     return render_to_response('admin/batch_report.html',{'form':form,},context_instance=RequestContext(request))

def postmortem_status(request,asset_code):
    username=request.user
    dep=Deployment.objects.filter(user=username)
    dep_path=dep[0].dep_path
    print dep_path
    from django.db.models.loading import get_model
    PostmortemImage = get_model(dep_path, 'PostmortemImage')
    vdata = PostmortemImage.objects.filter(asset_code__iexact=asset_code).order_by('-scan_time')
    c = str(vdata.count())
    total_records ="Total records: "+c
    paginator = Paginator(vdata, 20)
    page = request.GET.get('page')
    try:
     data = paginator.page(page)
    except PageNotAnInteger:
     data = paginator.page(1)
    except EmptyPage:
     data = paginator.page(paginator.num_pages)
    return render_to_response('admin/postmortem_status.html', {
            'data': data,'pdata':vdata,"total_records":total_records
            },context_instance=RequestContext(request))

def download_mediabook(request):
    dep = Deployment.objects.filter(user=request.user)
    dep_path = dep[0].dep_path
    from django.db.models.loading import get_model
    Verification = get_model(dep_path, 'Verification')
    Registration = get_model(dep_path, 'Registration')
    ActivityLog = get_model(dep_path, 'ActivityLog')
    from core.utils import get_ip,get_address
    if request.method == 'POST':
       form = DateRangeForm(request.POST)
       if form.is_valid():
        username=str(request.user)
        d1 = form.cleaned_data['day1']
        d2 = form.cleaned_data['day2']
        status = form.cleaned_data['status']
        if d1<=d2:
          if status=='Registration':
           queryset=Registration.objects.filter(scan_time__range=(d1, d2),status=1).order_by('-scan_time')#+datetime.timedelta(days=1))).order_by('-scan_time')
          elif status=='Verification':
           queryset=Verification.objects.filter(scan_time__range=(d1, d2)).order_by('-scan_time').exclude(status=1)
          print "counter:",queryset.count()
          if queryset.count()>0 and queryset.count()<10000:
           c=get_address(request)
           response=export_media2(queryset,username)
           al=ActivityLog(staff=str(request.user),activity_time=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),ip_address=get_ip(request),city=c['city'],postal_code=c['postal_code'],remark="media records exported!")
           al.save()
           return response
          elif queryset.count()>10000:
           message="File size for this range will be too big to export, please select lower date-time range"
           return render_to_response('admin/export_media.html', {'form':form,'message':message},context_instance=RequestContext(request))
          else:
           message="No data found with in the range!"
           return render_to_response('admin/export_media.html', {'form':form,'message':message},context_instance=RequestContext(request))
        else:
          message="Invalid date-time entry"
          return render_to_response('admin/export_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
       else:
        message="Invalid date-time entry"
        return render_to_response('admin/export_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
    else:
     form = DateRangeForm()
     return render_to_response('admin/export_media.html', {'form':form,},context_instance=RequestContext(request))

from core.utils import queryset_to_workbook
def download_workbook(request):
     dep = Deployment.objects.filter(user=request.user)
     dep_path = dep[0].dep_path
     from django.db.models.loading import get_model
     Verification = get_model(dep_path, 'Verification')
     Registration = get_model(dep_path, 'Registration')
     ActivityLog = get_model(dep_path, 'ActivityLog')
     from core.utils import get_ip,get_address
     if request.method == 'POST':
         form = DateRangeForm(request.POST)
         if form.is_valid():
          d1 = form.cleaned_data['day1']
          d2 = form.cleaned_data['day2']
          status = form.cleaned_data['status']
          if d1<=d2:
           if status=='Registration':
            print 'Registration'
            queryset=Registration.objects.filter(scan_time__range=(d1, d2),status=1).order_by('-scan_time')#+datetime.timedelta(days=1))).order_by('-scan_time')
           elif status=='Verification':
            print 'Verification'
            queryset=Verification.objects.filter(scan_time__range=(d1, d2)).order_by('-scan_time').exclude(status=1)
           columns = (
                   'asset_code',
                   'scan_time',
                   'status',
                   'city',
                   'auth_code',
                   'product_details',
                   'operator',
                   'bit_mask',
                   'image')
           print "counter:",queryset.count()
           if queryset.count()>0 and queryset.count()<65535:
            c=get_address(request)
            message="Total "+str(queryset.count())+" records found in provided range"
            workbook = queryset_to_workbook(queryset, columns)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="export_data.xls"'
            workbook.save(response)
            al=ActivityLog(staff=str(request.user),activity_time=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),ip_address=get_ip(request),city=c['city'],postal_code=c['postal_code'],remark="data records exported!")
            al.save()
            if 'Display' in request.POST:
             return render_to_response('admin/export_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
            else:
             return response
           elif queryset.count()>65536:
            if 'Display' in request.POST:
              message="Total "+str(queryset.count())+" records found in provided range"
            else:
              message="File size for this range will be too big to export, please select lower date-time range"
            return render_to_response('admin/export_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
           else:
            message="No data found with in the range!"
            return render_to_response('admin/export_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
          else:
           message="Invalid date-time entry"
          return render_to_response('admin/export_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
         else:
          message="Invalid date-time entry"
          return render_to_response('admin/export_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
     else:
         form = DateRangeForm()
         return render_to_response('admin/export_data.html', {'form':form,},context_instance=RequestContext(request))

def settings(request):
    url_path="/admin/core/configuration/"
    return HttpResponseRedirect(url_path)

def settings_configure(request):
    if request.method == 'POST':
     message=""
     form = SettingsForm(request.POST)
     print "form object"
     if form.is_valid():
      dep_name=str(form.cleaned_data['dep_name'])
      dep_type=str(form.cleaned_data['dep_type'])
      email_host=str(form.cleaned_data['email_host'])
      email_port=str(form.cleaned_data['email_port'])
      email_username=str(form.cleaned_data['email_username'])
      email_password=str(form.cleaned_data['email_password'])
      data = {}
      data['email_host'] = email_host
      data['email_port']=email_port
      data['email_username'] = email_username
      data['email_password'] = email_password
      data['dep_name'] = dep_name
      data['dep_type'] = dep_type
      print dep_name,dep_type,email_host,email_port,email_username,email_password
      print data
      # Writing JSON data
      from core.get_json import getJSON
      getJSON(email_host,email_port,email_username,email_password,dep_name,dep_type)
      return HttpResponseRedirect("/settings/")
     else:
      message="Invalid Entry"
      form = SettingsForm()
      return render_to_response('admin/settings_configure.html',{'form':form,'message':message,},context_instance=RequestContext(request))
    else:
     form = SettingsForm()
     return render_to_response('admin/settings_configure.html',{'form':form,},context_instance=RequestContext(request))

def update_product_details(request):
	message=''
	if request.method == 'POST':
		form = UpdateProductDetailsForm(request.POST,request.FILES)
		if form.is_valid():
			dep_path = Deployment.objects.filter(user=request.user)[0].dep_path
			from django.db.models.loading import get_model
			Registration = get_model(dep_path, 'Registration')
			update_method=form.cleaned_data['update_method']
			if update_method=="dynamic":
				excel_file = request.FILES['excel_file']
				i=0
				try:
					import tempfile
					import xlrd
					fd, tmp = tempfile.mkstemp()
					with os.fdopen(fd, 'w') as out:
						out.write(excel_file.read())
					book=xlrd.open_workbook(tmp)
					sh = book.sheet_by_index(0)
					if sh.nrows<10002:
						for rx in range(1,sh.nrows):
							try:
								pd_max_length=Registration._meta.get_field('product_details').max_length
								obj=Registration.objects.get(asset_code=str(sh.row(rx)[0].value).rstrip('0').rstrip('.'),status=1)
								obj.product_details=str(sh.row(rx)[1].value)[:pd_max_length]
								obj.save()
								i=i+1;
							except Registration.DoesNotExist:
								obj = None
						message='Product details of '+str(i)+' row(s) updated successfully'
					else:
						message='Batch size is too big, file contains '+str(sh.nrows-1)+' records, please try less than 10000'
				finally:
					os.unlink(tmp)
			else:
				prefix=form.cleaned_data['prefix']
				start_id=form.cleaned_data['start_id']
				end_id=form.cleaned_data['end_id']
				product_detail=form.cleaned_data['product_detail']
				i=0
				if len(start_id)==len(end_id) and str(start_id).isdigit() and str(end_id).isdigit():
					if int(end_id)>int(start_id):
						batch_count=int(end_id)-int(start_id)
						if batch_count<=100000:
							for ids in range(int(start_id),int(end_id)+1):
								asset_id=prefix+str(ids).zfill(len(str(start_id)))
								try:
									obj=Registration.objects.get(asset_code=asset_id,status=1)
									obj.product_details=product_detail
									obj.save()
									i=i+1;
								except Registration.DoesNotExist:
									obj = None
							message='Product details of '+str(i)+' row(s) updated successfully'
						else:
							message='Batch size is too big, please try less than 100000'
					else:
						message='End ID should be bigger than Start ID'
				else:
					message='Invalid Start ID or End ID, length of both should be same and only numbers allowed'
		else:
			message='Invalid Entries'
	else:
		form = UpdateProductDetailsForm()
	return render_to_response('admin/import_data.html', {'form':form,'message':message},context_instance=RequestContext(request))
