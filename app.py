import os

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

import urllib.request

app = Flask(__name__)

CORS(app, support_credentials=True)

pg_db = os.getenv("PG_DB")
secret = os.getenv("SECRET_KEY")
salt = os.getenv("BCRYPT_SALT")

app.config["JWT_SECRET_KEY"] = secret
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = pg_db
db = SQLAlchemy(app)
CORS(app)

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"User: {self.User}"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        # Add Bcrypt when you have time...
    

# def _build_cors_preflight_response():
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response

@app.route('/auth', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = User.query.filter_by(email=email)
    password = User.query.filter_by(password=password)
    if test and password:
        access_token = create_access_token(identity=email)
        response = {"access_token":access_token}
        return response

@app.route('/register', methods=["POST"])
def create_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
 
    new_user = User(email, password)
    db.session.add(new_user) 
    db.session.commit()   
    return jsonify({'message': 'registered successfully'})


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route('/tasks', methods=["POST", "GET"])
def task():
    if request.method == "POST":
        # _build_cors_preflight_response()
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
        # _build_cors_preflight_response()
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