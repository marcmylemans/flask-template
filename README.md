# Backend

## Settign up the Environment

1. Install Python

2. Create virtual Environment

```
python -m venv venv
```

And activate it with:

On Windows: 

```
venv\Scripts\activate
```

On MacOS/Linux: source 

```
venv/bin/activate
```

Installing all requirements:

```
pip install -r requirements.txt
```

## Creating a Basic Flask Application

1. Create Your Flask App:

Make a new directory for your project, and inside that, create a new Python file, app.py.
In app.py, write a basic Flask application:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

2. Create Templates Directory:

Inside your project directory, create a folder named templates.
Inside templates, create an index.html file. This will be your homepage.
Write basic HTML here:

```html
<!DOCTYPE html>
<html>
<head>
    <title>UniFi Dashboard</title>
</head>
<body>
    <h1>Welcome to the UniFi Controller Purchase Dashboard</h1>
    <!-- More HTML will go here -->
</body>
</html>
```

## Run Your Flask App:


In your terminal, navigate to your project directory and run:
```
python app.py
```

Visit http://127.0.0.1:5000/ in your browser to see your basic web page.


## Install python-digitalocean

```
pip install python-digitalocean
```


## Create a Registration Form
You can use Flask-WTF to create a registration form. If you haven't installed Flask-WTF, do it using:

```
pip install Flask-WTF
```


## installing the Database:

```
pip install Flask-SQLAlchemy Flask-Migrate
```

Set the FLASK_APP environment variable:

```
export FLASK_APP=app.py  # On Windows, use 'set' instead of 'export'
```

Initialize migrations (only once):

```
flask db init
```

Create the first migration:

```
flask db migrate -m "Initial migration."
```

Apply the migration to create database tables:

```
flask db upgrade
```

## Install the email_validator Package

```
pip install email_validator
```

## Creating a CronJob

Open your terminal.
Type crontab -e to edit the cron jobs.
Add a line at the end of the file to schedule your script. For example, to run it daily at midnight:

Open crontab:

```bash
crontab -e 
```
Adding the cronjob:

```bash
0 0 * * * /usr/bin/python3 /root/App/update_patreon_status.py
```
