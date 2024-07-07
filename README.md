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

1. Create the Blueprint File
   
Create a new file, e.g., new_module.py, and define your blueprint:

```python
from flask import Blueprint, render_template

new_module = Blueprint('new_module', __name__)

@new_module.route('/new')
def new_route():
    return render_template('new_module/new_route.html')

```

2. Create Template for the New Route
   
Create the necessary template file in templates/new_module/new_route.html:

```html
<!-- templates/new_module/new_route.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>New Module</title>
</head>
<body>
    <h1>Welcome to the New Module!</h1>
</body>
</html>
```

3. Register the New Blueprint
   
In app.py, import and register the new blueprint:

```python
from new_module import new_module as new_module_blueprint

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth'
app.register_blueprint(new_module_blueprint, url_prefix='/new_module')
```

4. Test the New Route
   
Run the application and navigate to http://127.0.0.1:5000/new_module/new to see your new module in action.

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
