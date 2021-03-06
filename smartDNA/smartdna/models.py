import datetime
from django.conf import settings
import os,datetime
from django.db import models
from core.utils import STATUS_CHOICES

PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
FILE_PATH=PROJECT_PATH+"smartDNA"

class VerificationManager(models.Manager):
    def get_queryset(self):
        return super(VerificationManager, self).get_queryset().filter(company_name='Demo')

class PeriodicScanAsset(models.Model):
   asset_code= models.CharField(verbose_name="Asset ID",max_length=32, default="")
   interval= models.CharField(verbose_name="Scan Interval",max_length=16,default="1")

class Verification(models.Model):
    asset_code = models.CharField(verbose_name="Asset-ID",max_length=32, default="",db_index=True)
    child_of = models.CharField(verbose_name="Parent Asset-ID ",max_length=32, default="NA",null=True,blank=True)
    scan_time=models.DateTimeField(verbose_name="Scan Time",default=datetime.datetime.now)#,auto_now_add=True)
    credential = models.CharField(verbose_name="Credential",max_length=16, default="")
    d1 = models.CharField(verbose_name="D1",max_length=8, default="0.0")
    d2 = models.CharField(verbose_name="D2",max_length=8, default="0.0")
    d3 = models.CharField(verbose_name="D3",max_length=8, default="0.0")
    h1 = models.CharField(verbose_name="H1",max_length=8, default="0.0")
    h2 = models.CharField(verbose_name="H2",max_length=8, default="0.0")
    h3 = models.CharField(verbose_name="H3",max_length=8, default="0.0")
    angle = models.CharField(verbose_name="Orientation",max_length=8, default="")
    status = models.IntegerField(verbose_name="Status",choices=STATUS_CHOICES,default=1,db_index=True)
    orr_credential=models.IntegerField(verbose_name="Forensic Credential",default=1000)
    operator = models.CharField(verbose_name="Operator",max_length=30, default="",db_index=True)
    geo_location = models.CharField(verbose_name="Geo-Location",max_length=64, default="")
    street = models.CharField(verbose_name="Address",max_length=64, default="")
    locality = models.CharField(verbose_name="Locality",max_length=128, default="")
    city = models.CharField(verbose_name="City",max_length=32, default="")
    state = models.CharField(verbose_name="State",max_length=32, default="")
    postal_code = models.CharField(verbose_name="Postal Code",max_length=16, default="")
    country = models.CharField(verbose_name="Country",max_length=16, default="")
    auth_code = models.CharField(verbose_name="Mobile Number",max_length=20, default="none")
    image =  models.FileField(upload_to='documents/')
    created = models.DateTimeField(verbose_name="Created on",blank=True,auto_now_add=True)
    modified = models.DateTimeField(verbose_name="Modified on",blank=True,auto_now=True)
    product_details= models.CharField(verbose_name="Dispatch ID",max_length=128, null=True,blank=True, default="Not Found")
    bit_mask = models.CharField(verbose_name="Bit Mask",max_length=64, null=True,blank=True, default="")
    color_profile = models.CharField(verbose_name="Color Profile",max_length=64, null=True,blank=True, default="")
    email_id = models.CharField(verbose_name="Recipient Email-ID",max_length=64, null=True,blank=True, default="")
    company_name = models.CharField(verbose_name="Company",max_length=64, null=True,blank=True, default="")

    objects = VerificationManager()

    class Meta:
        verbose_name_plural = 'Scan Monitoring'
        index_together = (('company_name','asset_code','product_details','auth_code','city','status','scan_time','id'),
        	('company_name','state','status','scan_time','id'),
        	('company_name','status','scan_time','id'),
        	('company_name','modified','scan_time','id','status'),)
   
    def save(self, *args, **kwargs):
        child_of=Registration.objects.filter(asset_code=self.asset_code)[0].child_of
        if child_of!='NA':
         self.child_of=child_of
        super(Verification, self).save(*args, **kwargs)

    def delete(self,*args,**kwargs):
	if self.pk:
	 image=self.image
         print image
	 if os.path.isfile(FILE_PATH+image.name) and image!="/media/documents/signature-not-found-4.png":
	  os.remove(FILE_PATH+image.name)
        super(Verification, self).delete()

    def release(self,*args,**kwargs):
        print "releasing the assets!"
        asset_code=self.asset_code
        print asset_code
        v=Verification.objects.filter(asset_code__exact=asset_code,status=1)
        for x in v:
            x.status=10
            x.save()

    def sps(self,*args,**kwargs):
        print "sps ",args[0]
        asset_code=self.asset_code
        print "sps ",asset_code
	psa=PeriodicScanAsset.objects.filter(asset_code=asset_code)
	if(psa.exists()):
	 for p in psa:
	  p.interval=args[0]
	  p.save()
	else:
         psa=PeriodicScanAsset(asset_code=asset_code,interval=args[0])
         psa.save()

    def __unicode_self_(self):
        return "%s" %(self.asset_code)

    def sms_credential(self):
        return "Barcode=%s-d1=%s-d2=%s-d3=%s-ag=%s-pd=%s-co=%s-st=%s" % (self.asset_code,self.d1,self.d2,self.d3,self.angle,self.product_details,self.company_name,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"))

    def total_credential(self):
        return "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (self.d1,self.d2,self.d3,self.angle,self.h1,self.h2,self.h3,self.product_details,self.company_name,self.color_profile,self.auth_code,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"))
    def track_trace_credential(self):
       if self.child_of=="none":
            v=Verification.objects.filter(child_of=self.asset_code)
            c='-'.join(v.values_list('asset_code',flat=True))
            return "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (self.d1,self.d2,self.d3,self.angle,self.h1,self.h2,self.h3,self.product_details,self.company_name,self.color_profile,self.auth_code,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"),c)
       else:
            p=self.child_of
            return "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (self.d1,self.d2,self.d3,self.angle,self.h1,self.h2,self.h3,self.product_details,self.company_name,self.color_profile,self.auth_code,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"),p)
    def colored_status(self):
        color=None
        if self.status==1:
            color="info"
        if self.status==12:
            color="warning"
        if  self.status==2 or self.status==13:
            color="success"
        if self.status==3 or self.status==4 or self.status==5 or self.status==14 or self.status==15:
            color="important"
        if color is None:
            color="inverse"
        return '<span class="badge badge-%s">%s</span>' % (color, STATUS_CHOICES[self.status-1][1])
    colored_status.allow_tags = True
    colored_status.short_description = 'Status'

    def colored_asset_code(self):
        color=None
        if self.orr_credential==1000:
            color="non-forensic"
        else:
            color="forensic"
        return '<span class="badge badge-%s">%s</span>'%(color,self.asset_code)
    colored_asset_code.allow_tags=True
    colored_asset_code.short_description ="Asset ID"

    def show_childs(self):
        if self.child_of=='none':
         selected='?child_of__exact='+self.asset_code
         return '<a href="%s">%s</a>' % (selected,'Show Childs')
        else:
         return self.child_of
    show_childs.allow_tags = True
    show_childs.short_description = 'Parent-ID'

    def colored_scan_time(self):
	bm=str(self.bit_mask).split('|')
        color=None
        if len(bm)>7 and bm[7]=='false':
            color="non-forensic"
        else:
            color="forensic"
        return '<span class="badge badge-%s">%s</span>'%(color,self.scan_time.strftime('%Y-%m-%d %r'))
    colored_scan_time.allow_tags=True
    colored_scan_time.short_description ="Scan Time"

    def thumbnail(self):
        onerror_image="this.src='/media/documents/signature-not-found-4.png'"
        return '<div class="thumbnail-container"><img class="thumbnail" src="%s" onerror="%s"/></div>' % (self.image,onerror_image)
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Image'


    def item_info(self):
	item_info=self.product_details
	try:
	 item_info=str(item_info).split('#')[0]
	except:
	 item_info=self.product_details
	return item_info

    def forensic_status(self):
	orr_status="non-forensic mode scan"
        if self.orr_credential==0:
         orr_status="Duplicate Label"
        elif self.orr_credential==1:
         orr_status="Original Label"
        elif self.orr_credential==2:
         orr_status="Scanning in dark"
        elif self.orr_credential==3:
         orr_status="Keep handset tilted down on label side and up on barcode side"
        return orr_status
    def admin_thumbnail(self):
        return u'<img src="%s" />' % (self.image.url)
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def mnumber(self):
        bm=str(self.bit_mask).split('|')
        if len(bm)>8 and bm[8]=='true':
           return '<em style="float: left;width: 100px;"><i class="icon-ok-circle"></i>%s</em>'%(self.auth_code)
        else:
           return '<em style="float:left;width:100px;">%s</em>'%(self.auth_code)
    mnumber.allow_tags = True
    mnumber.short_description = 'Mobile Number'

class Registration(models.Model):
    asset_code = models.CharField(verbose_name="Asset-ID",max_length=32, default="",db_index=True,unique=True)
    child_of = models.CharField(verbose_name="Parent Asset-ID ",max_length=32, default="NA",null=True,blank=True)
    scan_time=models.DateTimeField(verbose_name="Scan Time",default=datetime.datetime.now)#,auto_now_add=True)
    credential = models.CharField(verbose_name="Credential",max_length=16, default="")
    d1 = models.CharField(verbose_name="D1",max_length=8, default="0.0")
    d2 = models.CharField(verbose_name="D2",max_length=8, default="0.0")
    d3 = models.CharField(verbose_name="D3",max_length=8, default="0.0")
    h1 = models.CharField(verbose_name="H1",max_length=8, default="0.0")
    h2 = models.CharField(verbose_name="H2",max_length=8, default="0.0")
    h3 = models.CharField(verbose_name="H3",max_length=8, default="0.0")
    angle = models.CharField(verbose_name="Orientation",max_length=8, default="")
    status = models.IntegerField(verbose_name="Status",choices=STATUS_CHOICES,default=1,db_index=True)
    orr_credential=models.IntegerField(verbose_name="Forensic Credential",default=1000)
    operator = models.CharField(verbose_name="Operator",max_length=30, default="",db_index=True)
    geo_location = models.CharField(verbose_name="Geo-Location",max_length=64, default="")
    street = models.CharField(verbose_name="Address",max_length=64, default="")
    locality = models.CharField(verbose_name="Locality",max_length=128, default="")
    city = models.CharField(verbose_name="City",max_length=32, default="")
    state = models.CharField(verbose_name="State",max_length=32, default="")
    postal_code = models.CharField(verbose_name="Postal Code",max_length=16, default="")
    country = models.CharField(verbose_name="Country",max_length=16, default="")
    auth_code = models.CharField(verbose_name="Mobile Number",max_length=20, default="none")
    image =  models.FileField(upload_to='documents/')
    created = models.DateTimeField(verbose_name="Created on",blank=True,auto_now_add=True)
    modified = models.DateTimeField(verbose_name="Modified on",blank=True,auto_now=True)
    product_details= models.CharField(verbose_name="Dispatch ID",max_length=128, null=True,blank=True, default="Not Found")
    bit_mask = models.CharField(verbose_name="Bit Mask",max_length=64, null=True,blank=True, default="")
    color_profile = models.CharField(verbose_name="Color Profile",max_length=64, null=True,blank=True, default="")
    email_id = models.CharField(verbose_name="Recipient Email-ID",max_length=64, null=True,blank=True, default="")
    company_name = models.CharField(verbose_name="Company",max_length=64, null=True,blank=True, default="")

    objects = VerificationManager()

    class Meta:
        verbose_name_plural = 'Registrations'
        index_together = (('company_name','asset_code','product_details','auth_code','city','status','scan_time','id'),
            ('company_name','state','status','scan_time','id'),
            ('company_name','status','scan_time','id'),
            ('company_name','modified','scan_time','id','status'),)

    def delete(self,*args,**kwargs):
     if self.pk:
      image=self.image
      print image
      if os.path.isfile(FILE_PATH+image.name) and image!="/media/documents/signature-not-found-4.png":
       os.remove(FILE_PATH+image.name)
      super(Verification, self).delete()

    def release(self,*args,**kwargs):
        print "releasing the assets!"
        asset_code=self.asset_code
        print asset_code
        v=Registration.objects.filter(asset_code__exact=asset_code,status=1)
        for x in v:
            x.status=10
            x.save()

    def sps(self,*args,**kwargs):
     print "sps ",args[0]
     asset_code=self.asset_code
     print "sps ",asset_code
     psa=PeriodicScanAsset.objects.filter(asset_code=asset_code)
     if(psa.exists()):
      for p in psa:
       p.interval=args[0]
       p.save()
     else:
         psa=PeriodicScanAsset(asset_code=asset_code,interval=args[0])
         psa.save()

    def __unicode_self_(self):
        return "%s" %(self.asset_code)

    def sms_credential(self):
        return "Barcode=%s-d1=%s-d2=%s-d3=%s-ag=%s-pd=%s-co=%s-st=%s" % (self.asset_code,self.d1,self.d2,self.d3,self.angle,self.product_details,self.company_name,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"))

    def total_credential(self):
        return "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (self.d1,self.d2,self.d3,self.angle,self.h1,self.h2,self.h3,self.product_details,self.company_name,self.color_profile,self.auth_code,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"))

    def track_trace_credential(self):
       if self.child_of=="none":
            v=Registration.objects.filter(child_of=self.asset_code)
            c='-'.join(v.values_list('asset_code',flat=True))
            return "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (self.d1,self.d2,self.d3,self.angle,self.h1,self.h2,self.h3,self.product_details,self.company_name,self.color_profile,self.auth_code,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"),c)
       else:
            p=self.child_of
            return "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (self.d1,self.d2,self.d3,self.angle,self.h1,self.h2,self.h3,self.product_details,self.company_name,self.color_profile,self.auth_code,datetime.datetime.strptime(str(self.scan_time),"%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M:%S %p"),p)

    def colored_status(self):
        color=None
        if self.status==1:
            color="info"
        if self.status==12:
            color="warning"
        if  self.status==2 or self.status==13:
            color="success"
        if self.status==3 or self.status==4 or self.status==5 or self.status==14 or self.status==15:
            color="important"
        if color is None:
            color="inverse"
        return '<span class="badge badge-%s">%s</span>' % (color, STATUS_CHOICES[self.status-1][1])
    colored_status.allow_tags = True
    colored_status.short_description = 'Status'

    def colored_asset_code(self):
        color=None
        if self.orr_credential==1000:
            color="non-forensic"
        else:
            color="forensic"
        return '<span class="badge badge-%s">%s</span>'%(color,self.asset_code)
    colored_asset_code.allow_tags=True
    colored_asset_code.short_description ="Asset ID"

    def colored_scan_time(self):
     bm=str(self.bit_mask).split('|')
     color=None
     if len(bm)>7 and bm[7]=='false':
      color="non-forensic"
     else:
      color="forensic"
     return '<span class="badge badge-%s">%s</span>'%(color,self.scan_time.strftime('%Y-%m-%d %r'))
    colored_scan_time.allow_tags=True
    colored_scan_time.short_description ="Scan Time"

    def thumbnail(self):
        onerror_image="this.src='/media/documents/signature-not-found-4.png'"
        return '<div class="thumbnail-container"><img class="thumbnail" src="%s" onerror="%s"/></div>' % (self.image,onerror_image)
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Image'

    def show_childs(self):
        if self.child_of=='none':
         selected='?child_of__exact='+self.asset_code
         return '<a href="%s">%s</a>' % (selected,'Show Childs')
        else:
         return self.child_of
    show_childs.allow_tags = True
    show_childs.short_description = 'Parent-ID'

    def item_info(self):
     item_info=self.product_details
     try:
      item_info=str(item_info).split('#')[0]
     except:
      item_info=self.product_details
     return item_info

    def forensic_status(self):
     orr_status="non-forensic mode scan"
     if self.orr_credential==0:
      orr_status="Duplicate Label"
     elif self.orr_credential==1:
      orr_status="Original Label"
     elif self.orr_credential==2:
      orr_status="Scanning in dark"
     elif self.orr_credential==3:
      orr_status="Keep handset tilted down on label side and up on barcode side"
     return orr_status
    def admin_thumbnail(self):
        return u'<img src="%s" />' % (self.image.url)
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def mnumber(self):
        bm=str(self.bit_mask).split('|')
        if len(bm)>8 and bm[8]=='true':
           return '<em style="float: left;width: 100px;"><i class="icon-ok-circle"></i>%s</em>'%(self.auth_code)
        else:
           return '<em style="float:left;width:100px;">%s</em>'%(self.auth_code)
    mnumber.allow_tags = True
    mnumber.short_description = 'Mobile Number'

class PostmortemImage(models.Model):
      asset_code=models.CharField(verbose_name="Asset Code",max_length=32,default="")
      scan_time=models.DateTimeField(verbose_name="Time of Scan",default=datetime.datetime.now)
      case_type=models.CharField(verbose_name="Case",max_length=32,default="")
      result = models.CharField(verbose_name="Result",max_length=64, choices=[('Not Audited', 'Not Audited'), ('Audited-OK', 'Audited-OK'),('Audited-Discrepant','Audited-Discrepant')],default="Not Audited")
      imagefile = models.FileField(upload_to='postmortem_image/')
      class Meta:
        verbose_name_plural="Postmortem Images"

      def delete(self,*args,**kwargs):
	image=self.imagefile
	if os.path.isfile(FILE_PATH+image.name):
          os.remove(FILE_PATH+image.name)

class Anomaly(models.Model):
    asset_code = models.CharField(verbose_name="Asset Code",max_length=32, default="")
    scan_time=models.DateTimeField(verbose_name="Time of smartDNA scan",default=datetime.datetime.now)
    operator = models.CharField(verbose_name="Operator",max_length=16, default="NF")
    location = models.CharField(verbose_name="Location",max_length=64, default="NF")

    class Meta:
	verbose_name = 'Anomaly Record'


class Alert(models.Model):
    tracking_code=models.CharField(verbose_name="Tracking Code",max_length=32,default="")
    alert_message=models.CharField(verbose_name="Alert Message",max_length=64,default="")
    alert_time=models.DateTimeField(verbose_name="Scan Time",default=datetime.datetime.now)
    class Meta:
	verbose_name_plural = 'Scan Alert'

class AlertSubscriber(models.Model):
    subscriber=models.CharField(verbose_name="Subscriber Name",max_length=32,default="")
    phone=models.CharField(verbose_name="Mobile Number",help_text="optional",max_length=16,default="",blank=True,null=True)
    email=models.CharField(verbose_name="Email ID",max_length=64,default="")
    scr_status=models.CharField(verbose_name="Subscription Status",choices=[("Active", "Active"), ("Inactive","Inactive")], max_length=24,default=0)
    class Meta:
	verbose_name_plural="Alert Subscribers"

class ActivityLog(models.Model):
    staff = models.CharField(verbose_name="User",max_length=16, default="")
    activity_time=models.DateTimeField(verbose_name="Activity Time",default=datetime.datetime.now)
    operator = models.CharField(verbose_name="Operator",max_length=64, default="NF")
    ip_address= models.CharField(verbose_name="IP Address",max_length=16,default="NF")
    city = models.CharField(verbose_name="City",max_length=64,null=True,blank=True,default="NF")
    postal_code=models.CharField(verbose_name="Postal COde",max_length=16,null=True,blank=True,default="NF")
    remark=models.CharField(verbose_name="Remark",max_length=256,default="NF")
