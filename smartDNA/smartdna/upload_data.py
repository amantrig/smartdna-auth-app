import urllib
import urllib2
def syncdata(asset_code,scan_time,credential,status,d1,d2,d3,h1,h2,h3,angle,orrcredential,color_profile,location,operator,username,password,scan_auth,productDetails,bit_mask,email_id):
    print "syncing"
    url = 'http://ec2-54-204-121-213.compute-1.amazonaws.com:8004/register/'
    data = urllib.urlencode({'asset_code':asset_code, 'scan_time':scan_time,'credential':credential,'status':status,'d1':d1,'d2':d2,'d3':d3,'h1':h1,'h2':h2,'h3':h3,'angle':angle,'orrcredential':orrcredential,'color_profile':color_profile,'location':location,'operator':operator,'username':username,'password':password,'scan_auth':scan_auth,'productDetails':productDetails,'bit_mask':bit_mask,'email_id':email_id})
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = response.read()
    print result
