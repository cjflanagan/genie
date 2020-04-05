from flask import Flask, send_from_directory, request
from flask import render_template
from flask import jsonify
import datetime
import pdb
import statistics
from operator import itemgetter
import numpy as np
import csv
import random
import requests
from os import path
from bs4 import BeautifulSoup

app = Flask("genie")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    data = []
    with open("ExampleValues.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            datarow = row[1:]
            datarow.append(np.arange(15).tolist())
            datarow.append(np.sin(np.arange(15)).tolist())
            datarow.append(np.arange(15).tolist())
            datarow.append(random.sample(range(1, 100), 15))
            data.append(datarow)

    return render_template("list.html", data = data)

@app.route('/js/list.js')
def listjs():
    return send_from_directory("js", "list.js")

@app.route('/js/data.js')
def data_js():
    return send_from_directory("js", "data.js")

@app.route("/search")
def search():
    q = request.args.get("q")
    results = []
    if path.exists("search_results/" + q):
        with open("search_results/" + q, "r") as results_file:
            reader = csv.reader(results_file)
            for row in reader:
                results.append(row)
    else:
        response = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyAfIVyy0YivPzdEmrec8KlKRJz1bTSQgw0&cx=004315576993373726096:gkqhc3opbnm&q=" + q)
        print("MAKING REQUEST")
        data = response.json()
        for item in data["items"]:
            results.append([item["title"], item["link"]])
        with open("search_results/" + q, "w") as results_file:
            writer = csv.writer(results_file)
            for result in results:
                writer.writerow(result)

    return jsonify(results)

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
            measure_types = ["change", "relative change", "average change", "current", "variance", "std", "mean", "relative std", "number of growth years"]
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
                entity_measures.append((ent, data, y[-1] - y[0], y[-1] / y[0], np.mean(y[1:] / y[0:-1]), y[-1], np.var(y), np.std(y), np.mean(y), np.std(y) / np.mean(y), float((y[1:] / y[0:-1] > 1).sum())))
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

app.run(host = "0.0.0.0", port = 5000)
