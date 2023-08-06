# Flask & KDB (qPython3 | finos) 

A repo designed to how to connect your Flask app to a q/KDB+ process using the finos python/kdb library - [qPython3](https://github.com/finos/qPython)

## Install

```
pip install Flask-kdb
```

## Configuration

Thisis just a very basic showcase. Currently these envirnoment variables are used:

```
KDB_HOST
KDB_PORT
```

## Usage

Import the class FlaskKDB and initialize using by using the constructor:

```python
from flask import Flask
from flask_kdb import FlaskKDB

app = Flask(__name__)
app.config['KDB_HOST'] = 'localhost'
app.config['KDB_PORT'] = 5000
kdb = FlaskKDB(app)
```

or delayed initialisation (via init_app):

```python
app = Flask(__name__)
app.config['KDB_HOST'] = 'localhost'
app.config['KDB_PORT'] = 5000

kdb = FlaskKDB()
kdb.init_app(app)
```

The first method is uses a persistant DB connection object that can be imported when required. I implemented this from this answer from [toppatopvt on StackOverflow](https://stackoverflow.com/a/55537278)


# References
- [SO - toppatopvt & persistant connections](https://stackoverflow.com/a/55537278)