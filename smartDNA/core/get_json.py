import os
import json
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]

def getJSON(v1,v2,v3,v4,v5,v6):
    data = {}
    data['email_host'] = v1
    data['email_port']=v2
    data['email_username'] = v3
    data['email_password'] = v4
    data['dep_name'] = v5
    data['dep_type'] = v6
    # Writing JSON data
    with open(PROJECT_PATH+'smartDNA/media/settings.json', 'w') as f:
     json.dump(data, f)
    # Reading data back
    with open(PROJECT_PATH+'smartDNA/media/settings.json', 'r') as f:
     json_data = json.load(f)    
    print json_data['dep_name'],json_data['dep_type']
