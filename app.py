from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

import urllib.request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://michaelzalik:cessna210@localhost/michaelzalik'
db = SQLAlchemy(app)
CORS(app, support_credentials=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Task: {self.task}"

    def __init__(self, task):
        self.task = task

def format_task_json(task):
    return {
        "task": task.task,
        "id": task.id,
        "created_at": task.created_at
    }

@app.route('/tasks', methods=["POST", "GET"])
def task():
    if request.method == "POST":
        task_name = request.json['task']
        task = Task(task_name)
        db.session.add(task)
        db.session.commit()
        return format_task_json(task)

    tasks = Task.query.order_by(Task.id.asc()).all()
    task_list = []
    for task in tasks:
        task_list.append(format_task_json(task))
    return {'tasks': task_list}

@app.route('/tasks/<id>', methods=["PUT", "DELETE", "GET"])
def task_modification(id):
    if request.method == "PUT":
        task_find = Task.query.filter_by(id=id)
        task = request.json['task']
        task_find.update(dict(task = task, created_at = datetime.utcnow()))
        return {'task': format_task_json(task_find.one())}
    
    elif request.method == "DELETE":
        task = Task.query.filter_by(id=id).one()
        db.session.delete(task)
        db.session.commit()
        return 'Task Deleted!'

    elif request.method == "GET":
        task = Task.query.filter_by(id=id).one()
        format_task = format_task_json(task)
        return {'task': format_task}

    return "Task Not Found."

@app.route('/quotes', methods=["GET"])
def get_news():
    url = "http://programming-quotes-api.herokuapp.com/quotes/random"
    
    response = urllib.request.urlopen(url)
    data = response.read()

    return data;


if __name__ == '__main__':
    app.run(debug=True)