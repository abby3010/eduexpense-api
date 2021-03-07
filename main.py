from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "This is Coding Abby"


if __name__ == '__main__':
    # Call everyday at a given time
    # sched.add_job(increment_counter, 'cron', day='*', hour=14, minute=50, second=10)
    # sched.add_job(increment_counter, 'cron', day='*', hour=14, minute=50, second=15)
    # sched.add_job(increment_counter, 'cron', day='*', hour=14, minute=50, second=20)
    # sched.add_job(add_to_list, 'cron', day='*', hour='*', minute='5')
    # sched.start()
    app.run()
