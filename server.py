from flask import Flask
from flask import render_template
from connection import connection
import datetime
import pdb

app = Flask("genie")

@app.route("/")
def index():
    with connection:
        with connection.cursor() as cur:
            cur.execute("SELECT id, count FROM entities ORDER BY count DESC LIMIT 1000")
            return render_template("index.html", entities = cur.fetchall(), datetime = datetime.datetime.now())

app.run()
