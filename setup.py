import os,sys
import json
import subprocess

PROJECT_PATH=os.path.dirname(os.path.realpath(__file__))+"/smartDNA/"

with open(os.path.dirname(os.path.realpath(__file__))+"/"+sys.argv[1], 'r') as f:
 config_data = json.load(f)

dbpass=sys.argv[2].split('=')[1]
rootpass=sys.argv[3].split('=')[1]
add_dependencies=sys.argv[4].split('=')[1]

#print dbpass,rootpass

print config_data['site_name'],config_data['database_name'],config_data['deployment_port'],config_data['site_title']

def execute():
    if add_dependencies=='yes':
     #Copy dependencies.tar.gz to disk-packeges
     os.system('echo '+rootpass+' |'+'sudo -S cp '+os.path.dirname(os.path.realpath(__file__))+"/install/dependencies.tar.gz"+' '+config_data['python_path'])

     #change directory to disk-packages
     #os.system('cd /usr/local/lib/python2.7/dist-packages/')

     #Untar dependencies.tar.gz
     os.system('cd '+config_data['python_path']+' && '+'echo '+rootpass+' |'+'sudo -S tar -zxvf dependencies.tar.gz')
     os.system('cd '+config_data['python_path']+' && '+'echo '+rootpass+' |'+'sudo -S cp -r dependencies/. '+config_data['python_path'])

     #Delete dependencies.tar.gz and dependencies/
     os.system('echo '+rootpass+' |'+'sudo -S rm -r '+config_data['python_path']+'/dependencies/')
     os.system('echo '+rootpass+' |'+'sudo -S rm -r '+config_data['python_path']+'/dependencies.tar.gz')
    else:
     os.system('echo "dependencies not added..."')

    os.system('echo "setting-up sAMM portal"')

    os.system('cp '+PROJECT_PATH+'settings_sample.py'+' '+PROJECT_PATH+'settings.py')

    os.system("sed -i 's/DATABASE_NAME/"+config_data['database_name']+"/g' "+PROJECT_PATH+"settings.py")

    os.system("sed -i 's/DATABASE_PASSWORD/"+dbpass+"/g' "+PROJECT_PATH+"settings.py")

    os.system("sed -i 's/SITE_TITLE/"+config_data['site_title']+"/g' "+PROJECT_PATH+"settings.py")
    
    os.system("sed -i 's/DEPLOYMENT_HOST/"+config_data['deployment_host']+"/g' "+PROJECT_PATH+"settings.py")

    os.system('echo "enter database password for root user..."')

    #CREATE DATABASE mydatabase CHARACTER SET utf8 COLLATE utf8_general_ci;

    os.system('echo "create database '+config_data['database_name']+'" CHARACTER SET utf8 COLLATE utf8_general_ci | mysql -u root -p'+dbpass)

    #os.system('echo "create database '+config_data['database_name']+'" | mysql -u root -p'+dbpass)

    os.system('cd '+ PROJECT_PATH+' && python manage.py makemigrations smartdna')
    os.system('cd '+ PROJECT_PATH+' && python manage.py makemigrations core')
    os.system('cd '+ PROJECT_PATH+' && python manage.py migrate')
    os.system('cd '+ PROJECT_PATH+' && python manage.py createsuperuser')

    text_file = open(os.path.dirname(os.path.realpath(__file__))+"/"+config_data['site_name']+".conf", "w")
    text_file.write("<VirtualHost *:"+config_data['deployment_port']+">")
    text_file.write("\n\n\tWSGIScriptAlias / "+PROJECT_PATH+"smartdna.wsgi")
    text_file.write("\n\tAlias /static "+PROJECT_PATH+"static")
    text_file.write("\n\n\tErrorLog ${APACHE_LOG_DIR}/error.log")
    text_file.write("\n\t#Possible values include: debug, info, notice, warn, error, crit, alert, emerg.")
    text_file.write("\n\tLogLevel error")
    text_file.write("\n\tCustomLog ${APACHE_LOG_DIR}/access.log combined")
    text_file.write("\n\n\t<Directory "+PROJECT_PATH[:-1]+">")
    text_file.write("\n\t\t<Files smartdna.wsgi>")
    text_file.write("\n\t\t\tRequire all granted")
    text_file.write("\n\t\t</Files>")
    text_file.write("\n\t</Directory>")
    text_file.write("\n\n\t<Directory "+PROJECT_PATH+"static>")
    text_file.write("\n\t\tRequire all granted")
    text_file.write("\n\t</Directory>")
    text_file.write("\n\n\t# Use wsgi in daemon mode")
    text_file.write("\n\tWSGIDaemonProcess smartdna_"+config_data['site_name']
    	+" processes=2 threads=15 display-name=%{GROUP} "+"python-path="+PROJECT_PATH[:-1]
    	+":"+config_data['python_path'])
    text_file.write("\n\tWSGIProcessGroup smartdna_"+config_data['site_name'])
    text_file.write("\n</VirtualHost>")
    text_file.close()

    ports_file="/etc/apache2/ports.conf"
    ports_file_tmp="/tmp/ports.conf"
    c1= "NameVirtualHost *:"+config_data['deployment_port']
    c2= "Listen "+config_data['deployment_port']

    lines=[]
    with open(ports_file, 'rt') as f: 
     for line in f:
      cleanedLine = line.strip()
      if cleanedLine:
       lines.append(" ".join(cleanedLine.split()))

    #print lines
    f=open(ports_file, 'rt')
    s = f.read()

    if c1 in lines and c2 in lines:
     os.system('echo "apache is already listening on the port with virtual host"')
    elif c2 in lines:
     os.system('echo "apache is already listening on the port without virtual host"')
     outf=open(ports_file_tmp, 'w')
     outf.write(c1+"\n")
     outf.write(s)
     outf.close()
     os.system('echo '+rootpass+' |'+'sudo -S mv '+ports_file_tmp+' '+ports_file)
    elif c1 in lines:
     os.system('echo "apache already contain virtual host without listener on the port"')
     outf=open(ports_file_tmp, 'w')
     outf.write(c2+"\n")
     outf.write(s)
     outf.close()
     os.system('echo '+rootpass+' |'+'sudo -S mv '+ports_file_tmp+' '+ports_file)
    else:
     outf=open(ports_file_tmp, 'w')
     outf.write(c1+"\n")
     outf.write(c2+"\n")
     outf.write(s)
     outf.close()
     os.system('echo '+rootpass+' |'+'sudo -S mv '+ports_file_tmp+' '+ports_file)

    os.system('echo "enter root user password..."')
    os.system("echo "+rootpass+" |"+"sudo -S cp -r "+os.path.dirname(os.path.realpath(__file__))+"/"+config_data['site_name']+".conf"+" /etc/apache2/sites-available/")
    os.system('cd /etc/apache2/sites-available/ && sudo a2ensite '+config_data['site_name']+".conf")
    os.system('echo '+rootpass+' |'+'sudo -S service apache2 restart')
    os.system('echo '+rootpass+' |'+'sudo -S chmod -R 0777 '+PROJECT_PATH+'media/')
    os.system("echo "+rootpass+" |"+"sudo -S rm "+config_data['site_name']+".conf")

    #Update GeoIP.dat and GeoLiteCity.data

    os.system('cd '+PROJECT_PATH+' && '+'wget "http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz"')
    os.system('cd '+PROJECT_PATH+' && '+'wget "http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz"')
    os.system('cd '+PROJECT_PATH+' && '+'gunzip -kf GeoIP.dat.gz')
    os.system('cd '+PROJECT_PATH+' && '+'gunzip -kf GeoLiteCity.dat.gz')
    os.system('cd '+PROJECT_PATH+' && '+'rm GeoIP.dat.gz')
    os.system('cd '+PROJECT_PATH+' && '+'rm GeoLiteCity.dat.gz')

err,py_version= subprocess.Popen(['python', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
django_version = subprocess.check_output('python -c "import django; print(django.get_version())"', shell=True)

if "Python 2.7" in py_version and "1.8" in django_version:
 execute()
else:
 os.system('echo "Application is supported on Python 2.7 and Django 1.6, current installations:"')
 print " ".join(py_version.split())
 print "Django"," ".join(django_version.split())

