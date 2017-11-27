import os

def deployApp(depname):
    os.system("cp -r smartdna/ "+depname+" && python manage.py syncdb")
