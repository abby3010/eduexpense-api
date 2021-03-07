from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# from flask_apscheduler import APScheduler
app = Flask(__name__)

# scheduler instance
sched = BackgroundScheduler(daemon=True)


# Connect to database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def increment_counter():
    ''' The functions run to call data from APIs and is scheduled to run only once in a day '''
    db.collection(u'Users').document(u'abhayubhale.30@gmail.com').update({
        "count": firestore.Increment(1)
    })

    print("Counter Incremented")


def add_to_list():
    db.collection(u'Users').document(u'abhayubhale.30@gmail.com').update({
        "list": firestore.ArrayUnion([datetime.datetime.now()])
    })

@app.route('/')
def index():
    return "Hola Amigo!"


if __name__ == '__main__':
    # Call everyday at a given time
    # sched.add_job(increment_counter, 'cron', day='*', hour=14, minute=50, second=10)
    # sched.add_job(increment_counter, 'cron', day='*', hour=14, minute=50, second=15)
    # sched.add_job(increment_counter, 'cron', day='*', hour=14, minute=50, second=20)
    sched.add_job(add_to_list, 'cron', day='*', hour='*', minute='5')
    sched.start()
    app.run()
