from flask import Flask
from flask import render_template
from flask import jsonify
from connection import connection
import datetime
import pdb
import statistics
from operator import itemgetter
import numpy as np

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
            years = sorted([*year_counts])


            cur.execute("""
                SELECT name, year, count
                FROM entities
                WHERE name IN (
                    SELECT name
                    FROM entities
                    GROUP BY name
                    ORDER BY sum(count) DESC
                    LIMIT 20000)
                ORDER BY year;
            """)
            entity_counts = {}
            for entity in cur.fetchall():
                entity_counts.setdefault(entity[0], {})
                entity_counts[entity[0]][entity[1]] = float(entity[2]) / year_counts[entity[1]]

            entity_measures = []
            measure_types = ["change", "relative change", "average change", "current", "variance", "std", "mean", "relative std"]
            for ent in entity_counts:
                entity_count = entity_counts[ent]
                data = []
                counts = []
                for year in years:
                    if year in entity_count:
                        data.append(round(entity_count[year], 2))
                        counts.append(entity_count[year])
                    else:
                        data.append(None)

                y = np.array(counts)
                entity_measures.append((ent, data, y[-1] - y[0], y[-1] / y[0], np.mean(y[1:] / y[0:-1]), y[-1], np.var(y), np.std(y), np.mean(y), np.std(y) / np.mean(y)))

            entity_lists = []
            for i, type in enumerate(measure_types):
                for b in range(2):
                    entity_list = {
                        "type": type,
                        "desc": not b,
                        "years": years,
                        "data": []
                    }
                    sorted_list = sorted(entity_measures, reverse = not b, key = itemgetter(i + 2))[:20]
                    for entity in sorted_list:
                        entity_list["data"].append((entity[0], entity[1], round(entity[i + 2], 2)))
                    entity_lists.append(entity_list)
            return jsonify(entity_lists)

app.run()
