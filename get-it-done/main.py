from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

form = """

<!doctype html>
<html>
    <body>
       <form action='/newblog'>
       <label for="New Blog Title"> New Blog Title:</label>
       <br/>
       <br/>
       <input type="text" name="newblog_title"/>
       <br/>
       <br/>
        <textarea class="input" name='newblog_post' rows="20" cols="20" style= "height:150px; width:150px" ></textarea>
       <br/>
       <input type="submit" /> 
       </form>
    </body>
</html>      

"""
time_form = """
    <style>
        .error {{ color: red; }}
    </style>
    <h1>Validate Time</h1>
    <form method='POST'>
        <label>Hours (24-hour format)
            <input name="hours" type="text" value='{hours}' />
        </label>
        <p class="error">{hours_error}</p>
        <label>Minutes
            <input name="minutes" type="text" value='{minutes}' />
        </label>
        <p class="error">{minutes_error}</p>
        <input type="submit" value="Validate" />
    </form>
    """

@app.route('/validate-time')
def display_time_form():
    return time_form.format(hours='', hours_error='',
        minutes='', minutes_error='')


def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

@app.route('/validate-time', methods=['POST'])
def validate_time():

    hours = request.form['hours']
    minutes = request.form['minutes']

    hours_error = ''
    minutes_error = ''

    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        hours = ''
    else:
        hours = int(hours)
        if hours > 23 or hours < 0:
            hours_error = 'Hour value out of range (0-23)'
            hours = ''

    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
        minutes = ''
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = 'Minutes value out of range (0-59)'
            minutes = ''

    if not minutes_error and not hours_error:
        time = str(hours) + ':' + str(minutes)
        return redirect('/valid-time?time={0}'.format(time))
    else:
        return time_form.format(hours_error=hours_error,
            minutes_error=minutes_error,
            hours=hours,
            minutes=minutes) 

@app.route('/valid-time')
def valid_time():
    time = request.args.get('time')
    return '<h1> You submitted {0}. Thanks for submitting a valid time!<h1>'.format(time)
        

@app.route('/newblog')
def new_blogs():
    newblog_post = request.args.get('newblog_post', 'newblog_title')
    
    return '<h1> Blog Post </h1>' + form, newblog_post 

     

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

@app.route("/newpost/<name>")
def new_post(name):
    return render_template("newpost.html", name=name)

@app.route('/blog', methods=['POST', 'GET'])
def all_blogs():
    
    blog_post = request.form.get('task')
    blog_title = request.form.get('blog title')
     
    return redirect(url_for('all_blogs'))       


if __name__ == '__main__':
    app.run()
