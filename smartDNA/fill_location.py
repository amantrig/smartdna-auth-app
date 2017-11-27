
from core.models import Verification

def set_location():
	obj=Verification.objects.get(location='null')
	obj.location = ' Block, HRBR Layout, Kalyan Nagar, Bengaluru, Karnataka 560043,'
	obj.save()

set_location()
