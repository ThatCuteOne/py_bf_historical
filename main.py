from flask import Flask, render_template
from flask_apscheduler import APScheduler
import sched, time
from fetchStats import fetchStats
# from debugUtils import saysomething
import sqlUtils
from minutesSince import minutesSince

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)

# run function

@app.route("/")
def index():
    return render_template('index.html',
    players_online=sqlUtils.get_latest_stats()[2],
    last_updated=minutesSince(sqlUtils.get_latest_stats()[1]),
    raw_data=sqlUtils.graph_data()
    )

if __name__ == '__main__':
    fetchStats()  # Fetch stats once at startup
    # Add the job
    scheduler.add_job(id='Scheduled Task', func=fetchStats, trigger='interval', minutes=10)
    
    # Start the scheduler
    scheduler.start()
    
    # Start the Flask server
    # use_reloader=False is important! Otherwise, the scheduler might run twice.
    app.run(debug=True, use_reloader=False)