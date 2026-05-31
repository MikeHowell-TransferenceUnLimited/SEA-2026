from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from dotenv import load_dotenv
import sqlite3, os

app = Flask(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, os.getenv('DATABASE', 'data.db')),
    SECRET_KEY = os.getenv('SECRET_KEY', 'development key'),
    USERNAME=os.getenv('USERNAME','admin'),
    PASSWORD=os.getenv('PASSWORD', 'default')
))

def connect_db():
    """connects to the specific database."""
    rv=sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db=get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the current application contexst."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
      g.sqlite_db.close()      

@app.route('/')
def show_entries():
    db=get_db()
    cur=db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
    init_db()
    app.run()

