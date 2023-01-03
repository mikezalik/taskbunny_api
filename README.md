# taskbunny_api

Taskbunny_API is a Flask-based API that serves as the backend for a React productivity application.

## Usage 👩‍💻

To get started with this API, clone this repo and follow the steps below in your terminal:

```bash
git clone https://github.com/mikezalik/taskbunny_api.git
cd taskbunny_api
pip3 install -r requirements.txt
```

- **Development**: to run the API locally you'll need one terminal window/tab and a postgres instance. I use postgres.app to manage local DB instances. This app uses SQLAlchemy to interface with PostgreSQL databases. Utilize this snippet of Python code in app.py to connect the API to your DB.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/[YOUR_DATABASE_NAME]'
db = SQLAlchemy(app)
```

- **Build/Production**: The API may be accessed here: (https://taskbunnyapi.herokuapp.com/). See the Routes section for specifics on how to access each endpoint. Follow the steps below to deploy your own instance on heroku.

```bash
heroku login
heroku create
git push heroku main
heroku ps:scale web=1
heroku open
```

\*The instructions above assume no procfile has been created. In order to host on Heroku you'll need to use the following in your Procfile:

```procfile
web: gunicorn app:app
```

## Routes

Root URL: https://taskbunnyapi.herokuapp.com/

\*These endpoints should receive an html form, but will take JSON email and password for both registration and login.

- POST /auth
- POST /register
- POST /logout

\*User registration is required to access the endpoints below.

- POST /tasks
- GET /tasks
- GET /tasks/<id>
- PUT /tasks/<id>
- DELETE /tasks/<id>
- GET /quotes

## Project Summary

The taskbunny API is a Flask server that provides backend functionality for a React Frontend. The API accesses additional resources outside of taskbunny by calling third-party APIs and by serving JSON for tasks.

## Design Process 📐

I started designing taskbunny by thinking about the user journey. I reasoned that a robust microservice with protected endpoints would work to deliver JSON content and serve as an API for a React Frontend. I thought about future improvements and decided to implement Flask in a way that would promote extensibility.

## Development Process 🛠

I began with the base server and postgres configurations on my local device. I then created the models for tasks and users. After I tested these, I created routes and used Insomnia as a REST client to test each route. After each route was accessible without authentication, I implemented JWT and incorporated passport local strategies for both registration and login features. I reasoned that each endpoint should remain protected and I use the auth check middleware to verify authentication on each route.

## Tech Used 💻

### Back-End

- Python
- Flask
- PostgreSQL
- JSON Web Tokens - authentication

### Testing and Deployment

- [Heroku](https://www.heroku.com/) - cloud PaaS
- [Insomnia](https://insomnia.rest/) - REST client

## Ice Box

- Bcrypt
- Implement blueprints for modularity
- Add Foreign Keys
- Fix Netlify path so register/login feature works properly
