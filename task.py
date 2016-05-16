from flask import Flask, render_template, url_for
from taskw import TaskWarrior
from datetime import datetime
import pyjade

from date_helper import prettydate;

# TASKWARRIOR INIT

w = TaskWarrior()
tasks = w.load_tasks()
pending = tasks['pending']

# order by date
# if 'due' doesn't exist, then sort using the unix epoch
pending.sort(key=lambda x: datetime.strptime(x['due'], '%Y%m%dT%H%M%SZ') if 'due' in x else datetime.fromtimestamp(0))

# Get relative times for due dates
relatimes = []

got_dates = False
for task in pending:
    if 'due' in task:
        task_datetime = datetime.strptime(task['due'], "%Y%m%dT%H%M%SZ")
        relatime = prettydate(task_datetime)
        got_dates = True
    elif not got_dates:
        relatime = "is overdue"
    else:
        relatime = "none"
    relatimes.append(relatime)

# WEB

app = Flask(__name__)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/')
def index():
    return render_template('index.jade', title = "tasks",
            tasks = pending, dates = relatimes)

@app.route('/tasks')
def cakes():
    return 'le tasks!'

if __name__ == '__main__':
    app.run(debug=True)
