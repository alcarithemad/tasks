from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import session

from taskw import TaskWarrior
from datetime import datetime, timedelta
from base64 import b64encode
import humanize
import pyjade
import re
import os

# TASKWARRIOR INIT

w = TaskWarrior()
pending = []

def task_load():
    global pending
    global relatimes
    global realtimes
    global w
    tasks = w.load_tasks()
    pending = tasks['pending']

    large_date = datetime(9001, 1, 1)
    pending.sort(key=lambda x: datetime.strptime(x['due'], '%Y%m%dT%H%M%SZ') if 'due' in x else large_date)

    relatimes = []
    realtimes = []
    for task in pending:
        if 'due' in task:
            task_datetime = datetime.strptime(task['due'], "%Y%m%dT%H%M%SZ")
            realtime = task_datetime.strftime("%b %d %Y %H:%M:%S")
            relatime = humanize.naturaltime(datetime.now() - task_datetime)
        else:
            relatime = "no time"
            realtime = "no time"
        relatimes.append(relatime)
        realtimes.append(realtime)
    return

task_load()

# WEB SERVER

app = Flask(__name__)

if os.path.isfile('secret.txt'):
    with open('secret.txt') as f:
        app.secret_key = f.readline()
else:
    secret = os.urandom(24)
    utf_secret = b64encode(secret).decode('utf-8')
    with open('secret.txt', 'a') as secret_file:
        secret_file.write(utf_secret)
    app.secret_key = utf_secret

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

with open('cred.txt') as f:
    content = f.readlines()

user_pass = content[0].rstrip()

@app.before_request
def before_request():
    route = request.url_rule
    if ('logged' not in session):
        if request.path != '/login' and not re.match('/static/', request.path):
            return redirect(url_for('login'))

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
    realtime = realtimes[task_index]
    return render_template('task.jade', title = "task", index = task_index,
            task = current_task, due = relatime, real_due = realtime)

@app.route('/edit')
def edit():
    task_index = int(request.args.get('index'))
    current_task = pending[task_index]
    task_datetime = datetime.strptime(current_task['due'], "%Y%m%dT%H%M%SZ")
    task_date = task_datetime.strftime("%Y-%m-%d")
    task_time = task_datetime.strftime("%H:%M")
    return render_template('edit.jade', title = "task",
            task = current_task, t_date = task_date, t_time = task_time)

@app.route('/add')
def add():
    return render_template('add.jade', title = "add task")

@app.route('/sync')
def sync():
    w.sync()
    return redirect(url_for('index'))

def t_datetime(task_date, task_time):
    fdatetime = ""
    if task_date != "" and task_time != "":
        pseudo_datetime = task_date + task_time
        true_datetime = datetime.strptime(pseudo_datetime, "%Y-%m-%d%H:%M")
        fdatetime = true_datetime.strftime("%Y%m%dT%H%M%SZ")
    return fdatetime

@app.route('/action', methods=['GET', 'POST'])
def action():
    action = request.args.get('action')
    if request.method == "GET":
        if action == "done":
            w.task_done(id=int(request.args.get('id')))
            w.sync()
    elif request.method == "POST":
        action = request.form['action']
        if action == "add":
            task_description = request.form['description']
            if task_description != "":
                task_project = request.form['project']
                fdatetime = t_datetime(request.form['date'], request.form['time'])
                w.task_add(task_description, project=task_project, due=fdatetime)
        elif action == "update":
            task_id = request.form['id']
            id, current_task = w.get_task(id=task_id)

            current_task['description'] = request.form['description']
            current_task['project'] = request.form['project']

            fdatetime = t_datetime(request.form['date'], request.form['time'])
            current_task['due'] = fdatetime
            w.task_update(current_task)
    return redirect(url_for('index'))

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'logged' not in session:
        if request.method == 'POST':
            if request.form['pass'] == user_pass:
                session['logged'] = True;
                session.permanent = True
                return redirect(url_for('index'))
            else:
                error = 'true'
        return render_template('login.jade', error = error)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
