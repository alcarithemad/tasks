from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from taskw import TaskWarrior
from datetime import datetime
import humanize
import pyjade

# TASKWARRIOR INIT

w = TaskWarrior()
pending = []
relatimes = []

def task_load():
    global pending
    global relatimes
    global w
    tasks = w.load_tasks()
    pending = tasks['pending']

    large_date = datetime(9001, 1, 1)
    pending.sort(key=lambda x: datetime.strptime(x['due'], '%Y%m%dT%H%M%SZ') if 'due' in x else large_date)

    for task in pending:
        if 'due' in task:
            task_datetime = datetime.strptime(task['due'], "%Y%m%dT%H%M%SZ")
            relatime = humanize.naturaltime(datetime.now() - task_datetime)
        else:
            relatime = "no time"
        relatimes.append(relatime)
    return

task_load()

# WEB SERVER

app = Flask(__name__)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/')
def index():
    task_load()
    return render_template('index.jade', title = "overview",
            tasks = pending, dates = relatimes)

@app.route('/task')
def tasks():
    task_index = int(request.args.get('index'))
    current_task = pending[task_index]
    relatime = relatimes[task_index]
    return render_template('task.jade', title = "task",
            task = current_task, due = relatime)

@app.route('/sync')
def sync():
    w.sync()
    return redirect(url_for('index'))

@app.route('/action')
def action():
    action = request.args.get('action')
    task_id = int(request.args.get('id'))
    if action == "done":
        w.task_done(id=task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
