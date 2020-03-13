from flask import Flask
from flask import render_template
from flask import jsonify
from connection import connection
import datetime
import pdb
import statistics
from operator import itemgetter

app = Flask("genie")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/entities")
def entities():
    with connection:
        with connection.cursor() as cur:
            cur.execute("""
                SELECT extract(year FROM published_at) AS yyyy, count(*)
                FROM articles
                WHERE processed = true
                GROUP BY yyyy;
            """)

            year_counts = {}
            for year_count in cur.fetchall():
                year_counts[int(year_count[0])] = year_count[1]

            cur.execute("""
                SELECT name, year, count
                FROM entities
                WHERE name IN (
                    SELECT name
                    FROM entities
                    GROUP BY name
                    ORDER BY sum(count) DESC
                    LIMIT 500)
                ORDER BY year;
            """)
            ents = {}
            for entity in cur.fetchall():
                ents.setdefault(entity[0], ([], []))
                ents[entity[0]][0].append(entity[1])
                ents[entity[0]][1].append(entity[2] / float(year_counts[entity[1]]))

            ents_list = []
            for ent in ents:
                entity = ents[ent]
                ents_list.append((ent, entity[0], entity[1], (entity[1][-1] - entity[1][0]) ** 2), statistics.variance(entity[1]))

            ents_list = sorted(ents_list, reverse = True, key = itemgetter(4))[:50]
            return jsonify(ents_list)

app.run()
