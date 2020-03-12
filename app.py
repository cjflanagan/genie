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
            cur.execute("""
                SELECT name, year, count
                FROM entities
                WHERE name IN (
                    SELECT name
                    FROM entities
                    GROUP BY name
                    ORDER BY sum(count) DESC
                    LIMIT 500)
            """)

            entities = cur.fetchall()
            pdb.set_trace()

            return render_template("index.html", entities = cur.fetchall(), datetime = datetime.datetime.now())

app.run()
