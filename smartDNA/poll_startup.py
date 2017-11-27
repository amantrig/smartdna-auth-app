import os
import schedule
import time
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__))
def job():
    os.system('cd '+ PROJECT_PATH+' && python manage.py send_alert')

#def run():
schedule.every(10).minutes.do(job)
while True:
   schedule.run_continuously()
   time.sleep(1)
