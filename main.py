from flask import Flask, render_template
from flask_apscheduler import APScheduler
import sched, time
from fetchStats import fetchStats
import sqlUtils
from minutesSince import minutesSince

app = Flask(__name__)

# Initialize Scheduler
scheduler = APScheduler()
scheduler.init_app(app)

# --- CORRECTED SECTION ---
# Define and start the scheduler in the global scope so Gunicorn loads it.
if not scheduler.running:
    # Add the job
    scheduler.add_job(id='Scheduled Task', func=fetchStats, trigger='interval', minutes=10)
    
    # Start the scheduler
    scheduler.start()
    
    # Optional: Run an initial fetch immediately on startup
    # Note: Be careful with this if you have multiple workers (see below)
    try:
        fetchStats()
    except Exception as e:
        print(f"Initial fetch failed: {e}")
# -------------------------

@app.route("/")
def index():
    return render_template('index.html',
    players_online=sqlUtils.get_latest_stats()[2],
    last_updated=minutesSince(sqlUtils.get_latest_stats()[1]),
    raw_data=sqlUtils.graph_data()
    )

@app.route("/player/<username>")
def playerStats(username):
    return f'<p>Stats for player <strong>{username}<strong></p>'

@app.route("/stats_test")
def stats_test():
    fetchStats()
    return f'<p>Latest stats: {sqlUtils.get_latest_stats()[2]}</p>'

@app.route("/playersOverTime")
def players_over_time():
    return sqlUtils.two_cols_of_stats()

@app.route("/chart")
def chartPage():
    return render_template('e.html', raw_data=sqlUtils.graph_data())

if __name__ == '__main__':
    # You can keep this specifically for local testing if you want
    app.run(debug=True, use_reloader=False)