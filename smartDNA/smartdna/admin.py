import os
from django.contrib import admin
from django import forms
import datetime

depn=os.path.dirname(os.path.realpath(__file__)).split("/")[-1]
from django.db.models.loading import get_model
Anomaly=get_model(depn,'Anomaly')
Alert=get_model(depn,'Alert')
AlertSubscriber=get_model(depn,'AlertSubscriber')
Verification=get_model(depn,'Verification')
Registration=get_model(depn,'Registration')
ActivityLog=get_model(depn,'ActivityLog')
PostmortemImage=get_model(depn,'PostmortemImage')
PeriodicScanAsset=get_model(depn,'PeriodicScanAsset')
from core.models import Configuration,Deployment
from core.utils import trim_tuple
from core.forms import ScanIntervalForm
from core.filter import DateTimeRangeFilter
from django.conf import settings

print depn,PostmortemImage

demo_mode=settings.DEMO_MODE

def recent_scan_time(asset_code):
    allid = []
    allv=Verification.objects.filter(asset_code__exact=asset_code)
    for xv in allv:
        allid.append(xv.id)
    #print allid
    maxid=max(allid)
    mid=Verification.objects.get(id__exact=maxid)
    #print "recent Scan time ",mid.scan_time
    return mid.scan_time

class ViewModelAdmin(admin.ModelAdmin):
    change_form_template = 'admin/view_form.html'

    def changelist_view(self, request, extra_context=None):
        try:
            page_title = Verification._meta.verbose_name_plural.title()
            ctx = {'title': page_title}
            return super(ViewModelAdmin, self).changelist_view(request, extra_context=ctx)
        except:
            page_title = Verification._meta.verbose_name.title()
            ctx = {'title': page_title}
            return super(ViewModelAdmin, self).changelist_view(request, extra_context=ctx)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if demo_mode and str(request.user)=="admin":
        	extra_context['show_save'] = True
        	extra_context['show_tools'] = True
        else:
        	extra_context['show_save'] = False
        	extra_context['show_tools'] = False
        return super(ViewModelAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,)

    def has_delete_permission(self, request, obj=Verification()):
	    try:
	     if demo_mode and str(request.user)=="admin":
	      return True
	     else:
	      return False
	    except:
	     return False
    def has_add_permission(self, request):
	    try:
	     if demo_mode and str(request.user)=="admin":
	      return True
	     else:
	      return False
	    except:
	     return False

    def save_model(self, request, obj, form, change):
        #print request.user
	    try:
	     if demo_mode and str(request.user)=="admin":
	      super(VerificationAdmin, self).save_model(request, obj, form, change)
	     else:
	      print "not allowed to edit"
	    except:
	     print "Edit exception"

class VerificationAdmin(ViewModelAdmin):
    list_filter    = ('status','state',('modified',DateTimeRangeFilter))
    ordering       = ('-scan_time',)
    search_fields  = ('asset_code','product_details','auth_code','city')
    actions=['bulk_release']#,'set_periodic_scan']
    #action_form = ScanIntervalForm
    
    def get_list_display(self,request):
     #dep=Deployment.objects.filter(user=request.user)
     #dep_name=dep[0].dep_name
     config = Configuration.objects.filter(dep_name=1)[0]
     list_display = ('colored_asset_code','colored_scan_time','colored_status','modified','city','product_details','mnumber','operator','thumbnail')
     if config.dep_type=="Track-Trace":
      list_display = ('colored_asset_code','show_childs','colored_scan_time','colored_status','modified','city','product_details','mnumber','operator','thumbnail')
     return list_display

    def get_form(self, request, obj=None, **kwargs):
        form = super(VerificationAdmin, self).get_form(request, obj, **kwargs)
        if str(request.user)!="admin":
         self.exclude = ('d1','d2','d3','h1','h2','h3','angle','orr_credential')
        return form
        
    def get_actions(self, request):
        actions = super(VerificationAdmin, self).get_actions(request)
        if demo_mode and str(request.user)=="admin":
        	print "demo mode"
        else:
        	del actions['delete_selected']
        return actions

    def bulk_release(self,request,queryset):
        for obj in queryset:
            print "kukus kukus"
            obj.release()
        if queryset.count() == 1:
            message_bit="1 record "
        else:
            message_bit="%s records "%queryset.count()
        self.message_user(request, "%s successfully Released!" % message_bit)
    bulk_release.short_description = "Release Selected Entries"

    #def set_periodic_scan(self,request,queryset):
    #    for obj in queryset:
    #        print "setting periodic scan"
    #	    interval= request.POST['interval']
    #        obj.sps(interval)
    #    if queryset.count() == 1:
    #        message_bit="1 record "
    #    else:
    #        message_bit="%s records "%queryset.count()
    #    self.message_user(request, "%s successfully added in periodic scan table" % message_bit)
    #set_periodic_scan.short_description = "Set Periodic Scan"

class AlertAdmin(ViewModelAdmin):
    list_display=("tracking_code","alert_time","alert_message")
    ordering = ('-id',)
    search_fields  = ('tracking_code',)
    actions = None

class AlertSubscriberAdmin(admin.ModelAdmin):
    list_display = ('subscriber','email','phone','scr_status')
    ordering = ('-id',)

    def changelist_view(self, request, extra_context=None):
        try:
            page_title = AlertSubscriber._meta.verbose_name_plural.title()
            ctx = {'title': page_title}
            return super(AlertSubscriberAdmin, self).changelist_view(request, extra_context=ctx)
        except:
            page_title = AlertSubscriber._meta.verbose_name.title()
            ctx = {'title': page_title}
            return super(AlertSubscriberAdmin, self).changelist_view(request, extra_context=ctx)

class AnomalyAdmin(ViewModelAdmin):
    list_display=("asset_code","scan_time","operator","location")
    ordering = ('-id',)
    search_fields  = ('asset_code',)
    actions = None

class ActivityLogAdmin(ViewModelAdmin):
    list_display=("staff","activity_time","ip_address","city","postal_code","remark")
    ordering=('-id',)
    search_fields=("postal_code","remark",)
    actions = None

class PostmortemImageAdmin(ViewModelAdmin):
    list_display = trim_tuple(PostmortemImage._meta.get_all_field_names(),"id")
    actions = None

class PeriodicScanAssetAdmin(admin.ModelAdmin):
    list_display = trim_tuple(PeriodicScanAsset._meta.get_all_field_names(),"id")
    def get_actions(self, request):
      if str(request.user)=="admin":
       actions = super(PeriodicScanAssetAdmin, self).get_actions(request)
       return actions
      else:
       actions = super(PeriodicScanAssetAdmin, self).get_actions(request)
       del actions['delete_selected']
       return actions

    def has_delete_permission(self, request, obj=PeriodicScanAsset()):
     try:
      if str(request.user)=="admin":
          return True
      else:
          return False
     except:
         return True

    def has_add_permission(self, request):
     try:
      if str(request.user)=="admin":
          return True
      else:
          return False
     except:
         return True

    def save_model(self, request, obj, form, change):
     #print request.user
     try:
      if str(request.user)=="admin":
          super(PeriodicScanAssetAdmin, self).save_model(request, obj, form, change)
      else:
          print "not allowed to edit"
     except:
         print "Edit exception"
     #print request.user

admin.site.register(Registration,VerificationAdmin)
admin.site.register(Verification,VerificationAdmin)
admin.site.register(Alert,AlertAdmin)
admin.site.register(AlertSubscriber,AlertSubscriberAdmin)
admin.site.register(Anomaly,AnomalyAdmin)
admin.site.register(ActivityLog,ActivityLogAdmin)
admin.site.register(PostmortemImage,PostmortemImageAdmin)
admin.site.register(PeriodicScanAsset,PeriodicScanAssetAdmin,)

