from apscheduler.schedulers.blocking import BlockingScheduler
from getData import *
import datetime
import pytz

# Stock markets both NSE and BSE
# TIMING:  9:15 A.M. to 3:30 P.M
# DAYS: Monday to Friday


scheduler = BlockingScheduler()

tz = pytz.timezone('Asia/Kolkata')

scheduler.add_job(get_silver_rates, 'cron', day_of_week='mon-sun', hour='10', minute='35', timezone=tz)
scheduler.add_job(get_gold_rates, 'cron', day_of_week='mon-sun', hour='10', minute='36', timezone=tz)
scheduler.add_job(get_sensex, 'cron', day_of_week='mon-fri', hour='9-16', minute='*/5', timezone=tz)
scheduler.add_job(get_nifty, 'cron', day_of_week='mon-fri', hour='9-16', minute='*/5', timezone=tz)
scheduler.add_job(get_news, 'cron', hour='*', minute='0', timezone=tz)
scheduler.start()
print("Program Executed")
scheduler.start()
print("Program Executed")
