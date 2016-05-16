from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from functools import wraps
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

with open('cred.txt') as f:
    content = f.readlines()

user_name = content[0].rstrip()
user_pass = content[1].rstrip()

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == user_name and password == user_pass

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'GTFO!', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/')
@requires_auth
def index():
    task_load()
    return render_template('index.jade', title = "overview",
            tasks = pending, dates = relatimes)

@app.route('/task')
@requires_auth
def tasks():
    task_index = int(request.args.get('index'))
    current_task = pending[task_index]
    relatime = relatimes[task_index]
    return render_template('task.jade', title = "task",
            task = current_task, due = relatime)

@app.route('/add')
@requires_auth
def add():
    return render_template('add.jade', title = "add task")

@app.route('/sync')
@requires_auth
def sync():
    w.sync()
    return redirect(url_for('index'))

@app.route('/action', methods=['GET', 'POST'])
@requires_auth
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
