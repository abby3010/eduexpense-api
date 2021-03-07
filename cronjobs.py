from apscheduler.schedulers.blocking import BlockingScheduler

import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Connect to database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def timed_job():
    db.collection(u'Users').document(u'abhayubhale.30@gmail.com').update({
        "listTimed": firestore.ArrayUnion([datetime.datetime.now()])
    })
    print("Timestamp added to FIREBASE")

def scheduled_job():
    ''' The functions run to call data from APIs and is scheduled to run only once in a day '''
    db.collection(u'Users').document(u'abhayubhale.30@gmail.com').update({
        "count": firestore.Increment(1)
    })
    print("Counter Increased in FIREBASE")

scheduler = BlockingScheduler()

scheduler.add_job(timed_job, "interval", seconds=30)
scheduler.add_job(scheduled_job, 'cron', day='*', hour='*', minute='*', second=30)
scheduler.start()
