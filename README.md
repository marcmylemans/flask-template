# Backend

## Setting up the Environment

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

Initialize the Database:

```python
flask db init
flask db migrate
flask db upgrade
```

## Adding a New Module/Blueprint

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


## Running the Application with Docker

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Build and Run

1. Build the Docker image:
   
   ```bash
   docker-compose build
   ```
3. Run the Docker container:
   
   ```bash
   docker-compose up
   ```
The application will be accessible at http://localhost:5000.
