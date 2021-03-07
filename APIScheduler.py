from apscheduler.schedulers.background import BackgroundScheduler

import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Connect to database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

sched = BackgroundScheduler(daemon=True)

def scheduled_job():
    
    db.collection(u'Users').document(u'abhayubhale.30@gmail.com').update({
        "count": firestore.Increment(1)
    })

sched.add_job(scheduled_job, 'cron', day='*', hour='*', minute='2')
sched.start()