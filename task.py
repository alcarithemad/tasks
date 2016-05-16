from flask import Flask, render_template, url_for
from taskw import TaskWarrior
from datetime import datetime
import humanize
import pyjade

# TASKWARRIOR INIT

w = TaskWarrior()
tasks = w.load_tasks()
pending = tasks['pending']

# order by date
# if 'due' doesn't exist, then sort using a large date
# so the task gets ordered to the bottom
large_date = datetime(9001, 1, 1)
pending.sort(key=lambda x: datetime.strptime(x['due'], '%Y%m%dT%H%M%SZ') if 'due' in x else large_date)

# Get relative times for due dates
relatimes = []

got_dates = False
for task in pending:
    if 'due' in task:
        task_datetime = datetime.strptime(task['due'], "%Y%m%dT%H%M%SZ")
        relatime = humanize.naturaltime(datetime.now() - task_datetime)
        # relatime = timesince(task_datetime)
        got_dates = True
    elif not got_dates:
        relatime = "is overdue"
    else:
        relatime = "none"
    relatimes.append(relatime)

# WEB SERVER

app = Flask(__name__)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/')
def index():
    return render_template('index.jade', title = "overview",
            tasks = pending, dates = relatimes)

@app.route('/tasks')
def tasks():
    return render_template('task.jade', title = "task",
            tasks = pending, date = relatimes)

if __name__ == '__main__':
    app.run(debug=True)
