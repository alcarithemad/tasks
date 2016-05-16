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

def task_load():
    global pending
    global relatimes
    global w
    tasks = w.load_tasks()
    pending = tasks['pending']

    large_date = datetime(9001, 1, 1)
    pending.sort(key=lambda x: datetime.strptime(x['due'], '%Y%m%dT%H%M%SZ') if 'due' in x else large_date)

    relatimes = []
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

@app.route('/add')
def add():
    return render_template('add.jade', title = "add task")

@app.route('/sync')
def sync():
    w.sync()
    return redirect(url_for('index'))

@app.route('/action', methods=['GET', 'POST'])
def action():
    action = request.args.get('action')
    if request.method == "GET":
        if action == "done":
            task_id = int(request.args.get('id'))
            w.task_done(id=task_id)
    elif request.method == "POST":
        action = request.form['action']
        if action == "add":
            task_description = request.form['description']
            task_project = request.form['project']
            task_date = request.form['date']
            task_time = request.form['time']
            fdatetime = ""
            if task_date != "" and task_time != "":
                pseudo_datetime = task_date + task_time
                true_datetime = datetime.strptime(pseudo_datetime, "%Y-%m-%d%H:%M")
                fdatetime = true_datetime.strftime("%Y%m%dT%H%M%SZ")
            w.task_add(task_description, project=task_project, due=fdatetime)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
