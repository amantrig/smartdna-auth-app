from django.shortcuts import render_to_response,HttpResponse,HttpResponseRedirect
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from core.models import Deployment

def get_last_status(request):
    list_display=[]
    dep = Deployment.objects.filter(user=request.user)
    dep_path = dep[0].dep_path
    from django.db.models.loading import get_model
    try:
     Verification = get_model(dep_path, 'Verification')
     verification=Verification.objects.values('asset_code').distinct().order_by('-id')
     for s in [3,5,8,2]:
        list_display.append(verification.filter(status=s).count())
        verification=verification.exclude(asset_code__in=verification.filter(status=s).values_list('asset_code'))
     raw_string='{"cols": [{"id":"","label":"Topping","pattern":"","type":"string"},{"id":"","label":"Slices","pattern":"","type":"number"}],"rows": [{"c":[{"v":"Registered","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Tampered","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Discrepant","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Verified","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Label Error","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Released","f":null},{"v":%s,"f":null}]}]}' % ('0',list_display[0],list_display[1],list_display[3],list_display[2],'0')
     return HttpResponse(raw_string, content_type="application/json")
    except:
     return HttpResponse('none', content_type="application/json")

def live_chart_data(request):
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
     raw_string='{"cols": [{"id":"","label":"Topping","pattern":"","type":"string"},{"id":"","label":"Slices","pattern":"","type":"number"}],"rows": [{"c":[{"v":"Registered","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Tampered","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Discrepant","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Verified","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Label Error","f":null},{"v":%s,"f":null}]},{"c":[{"v":"Released","f":null},{"v":%s,"f":null}]}]}' % (rRows,tRows,dRows,vRows,eRows,aRows)
     return HttpResponse(raw_string, content_type="application/json")
    except:
     return HttpResponse('none', content_type="application/json")

def main(request):
    return render_to_response('analytics/dashboard.html',context_instance=RequestContext(request))