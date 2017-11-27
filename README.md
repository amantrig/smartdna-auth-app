# README #

smartdna-auth-app is an enterprise Security-as-a-Service (SaaS) application which serve as authentication backend for smartdna-scanning application (client application) with many other analytical features.



Follow the steps below to deploy the application:

##Setting-up the environment (Python, Django, Apache with WSGI and MySQL)##

#installing essential tools and dependencies
```
#!linux

$ python -V or pythonx -V #Check python version, if found python2.7 go without python2.7 installation step else install python2.7
$ sudo apt-get install python2.7 # Install Python2.7 
$ wget https://bootstrap.pypa.io/get-pip.py && sudo python get-pip.py # Install pip tool
$ sudo apt-get install build-essential libssl-dev libcurl4-gnutls-dev  libexpat1-dev gettext zip unzip # Install essential packages
$ sudo apt-get install git # Install git
$ git --version
```
#Install virtual env, create virtual env with python2.7 and activate virtual env to be used for django project

```
#!linux

$ sudo pip install virtualenv
$ mkdir ENVS && cd ENVS
$ virtualenv -p /usr/bin/python2.7 samm-virt-env # Make sure python executable path is correct
$ source samm-virt-env/bin/activate
```
# Install other necessary libraries
```
#!linux
$ sudo apt-get build-dep python-imaging
$ sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
$ sudo apt-get install libmysqlclient-dev
$ sudo apt-get install python-dev 
```
# Installing django and other essential site-packages
```
#!linux
$ pip install django==1.8 # Install django 1.8
$ pip install Pillow
$ pip install MySQL-python
$ pip install xlrd
```
#Installing Apache2

```
#!linux


$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi
$ sudo a2enmod wsgi
$ chmod o+x /home/user && ls -l /home/ # To avoid forbidden access error while running django app from home (non-root) directory with apache2
$ sudo service apache2 restart
```
Installing MySQL database
----------------------------

```
#!linux

$ sudo apt-get install mysql-server
```
MySQL optimizations
----------------------------

Add below mentioned lines in file /etc/mysql/mysql.conf.d/mysqld.cnf under [mysqld] tag:
```
#!linux

[mysqld]

key_buffer_size         = 32M
max_allowed_packet      = 32M

.....
.....
.....

innodb_file_per_table
innodb_flush_method=O_DIRECT
innodb_log_file_size=128M
innodb_buffer_pool_size=512M

```

##Deploying sAMM##

```
#!linux

$ mkdir dir_name
$ cd dir_name/
$ git clone -b master https://pradeep_verma9294@bitbucket.org/pradeep_verma9294/smartdna-auth-app.git
$ cd smartdna-auth-app/
```



Edit config.json and set the credentials as per availability.
Config.json
---------------
            {
            "site_name":"000-default.conf",
            "site_title": "Linksmart- sAMM Portal",
            "database_name": "smartdnadb",
            "deployment_host":"127.0.1.1",
            "deployment_port":"80",
            "python_path":"/home/usr/ENVS/smartdna-virt-env/local/lib/python2.7/site-packages"
            }

Running setup.py
----------------------
Run the command mentioned below and enter super-user details once asked
```
#!linux

$ python setup.py install/config.json --dbpassword=<secret> --userpassword=<secondsecret> --disk_pack=yes/no
```


###Post Installation steps###
Adding additional info of admin user
------------------------------------------
![Screenshot_from_2016-12-21_04_56_52.png](https://bitbucket.org/repo/eLrq6K/images/1361381035-Screenshot_from_2016-12-21_04_56_52.png)

Adding deployment (admins's profile) configuration
--------------------------------------------------
![Screenshot from 2017-02-03 17-50-24.png](https://bitbucket.org/repo/eLrq6K/images/2714239866-Screenshot%20from%202017-02-03%2017-50-24.png)

Creating group with permission for particular app
-------------------------------------------------------

```
#!linux
$ cd smartDNA/
$ python manage.py add_group smartdna dep_admin media/fixtures/permissions.json
```
![Screenshot_from_2016-12-17_04_48_51.png](https://bitbucket.org/repo/eLrq6K/images/379217983-Screenshot_from_2016-12-17_04_48_51.png)

Adding new User
---------------------
It is two step process

-  Adding user in auth/user/ table (consider adding to group and making staff if want to provide access to portal)
-  Adding additional information of user (like deployment belong to) in core/deployment/ table


Updating GeoIP database (First Wednesday of every month)
---------------------
```
#!linux
$ cd /home/samm/linksmart/smartdna-auth-app && python manage.py update_geodb
```

*Done...

Screenshot
![screenshot-smartdna-auth-app.png](https://bitbucket.org/repo/eLrq6K/images/1860917790-screenshot-smartdna-auth-app.png)