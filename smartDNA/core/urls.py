from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from core import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   #APIs
   url(r'^login$',views.login,name='login'),
   url(r'^fetch$',views.fetch,name='fetch'),
   url(r'^fetch_track_trace/$',views.fetch_track_trace,name='fetch_track_trace'),
   url(r'^sms_fetch/$',views.sms_fetch,name='sms_fetch'),
   url(r'^register/$',views.register,name='register'),
   url(r'^json_register/$',views.json_register,name='json_register'),
   url(r'^track_trace_register/$',views.track_trace_register,name='track_trace_register'),
   url(r'^upload_image/$',views.upload_image,name='upload_image'),
   url(r'^upload_postmortem_image/$',views.upload_postmortem_image,name='upload_postmortem_image'),
   url(r'^anomaly_register/$',views.anomalyReg,name='anomaly_register'),
   #Portal Views
   url(r'^$',views.monitoring,name='monitoring'), 
   url(r'^audit_monitoring/$',login_required(views.audit_monitoring),name='audit_monitoring'),
   url(r'^registration_monitoring/$',login_required(views.registration_monitoring),name='registration_monitoring'),
   url(r'^monitoring/$',login_required(views.cmonitoring),name='cmonitoring'),
   url(r'^scan_monitoring/$',views.scanmonitoring,name='scan_monitoring'),
   url(r'^status/(?P<code>\w{0,50})/',views.asset_status,name='status'),
   url(r'^orr_status/(?P<asset_code>\w{0,50})/',views.orr_status,name='orr_status'),
   url(r'^postmortem_status/(?P<asset_code>\w{0,50})/',views.postmortem_status,name='postmortem_status'),
   url(r'^support/$',login_required(views.support),name='support'), 
   url(r'^analytics/$',login_required(views.analytics),name='analytics'),
   url(r'^dashboard/$',login_required(views.dashboard),name='dashboard'),
   url(r'^batch_report/$',login_required(views.batch_report),name='batch_report'),
   url(r'^settings/$',login_required(views.settings),name='settings'),
   url(r'^settings_configure/$',login_required(views.settings_configure),name='settings_configure'),
   url(r'^download_mediabook/$',login_required(views.download_mediabook),name='download_mediabook'),
   url(r'^download_databook/$',login_required(views.download_workbook),name='download_databook'),
   url(r'^live_chart_data/$',login_required(views.live_chart_data),name='live_chart_data'),
   url(r'^update_product_details/$',login_required(views.update_product_details),name='update_product_details'),
) 
