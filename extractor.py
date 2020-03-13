import pdb
import connection
import csv
import tarfile
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import psycopg2
import shutil
import spacy
import datetime

url = "ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/"
nlp = spacy.load("en_core_sci_sm")

while True:
    with connection.connection as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT published_at FROM articles OFFSET floor(random() * %s) LIMIT 1;", (connection.articles_count,))
            year = cur.fetchone()[0].year

            cur.execute("""
                SELECT id, filename, published_at
                FROM articles
                WHERE processed = false
                AND published_at BETWEEN %s AND %s
                ORDER BY published_at
                DESC LIMIT 10;
            """, (datetime.datetime(year, 1, 1).date(), datetime.datetime(year + 1, 1, 1).date()))

            articles = cur.fetchall()
            ents = {}

            for article in articles:
                try:
                    response = urllib.request.urlopen(url + article[1])
                    tar = tarfile.open(fileobj=response, mode="r:gz")
                    tar.extractall("/tmp/genie/")
                    name = [n for n in tar.getnames() if n[-3:] == "xml"][0]
                    file = open("/tmp/genie/" + name, "r")
                    content = file.read()
                    file.close()
                    shutil.rmtree("/tmp/genie/" + tar.getmembers()[0].name)
                    tar.close()

                    tree = ET.fromstring(str(content))
                    abstract = tree[0][1].find("abstract")
                    abstract = ET.tostring(abstract, method = "text").decode()
                    for ent in nlp(abstract).ents:
                        ents[ent.text.lower()] = ents.get(ent.text.lower(), 0) + 1
                except:
                    print("error in " + article[0])

            if len(ents):
                entities = {}

                cur.execute("SELECT name, count FROM entities WHERE name IN %s AND year = %s;", (tuple([*ents]), year))
                for entity in cur.fetchall():
                    entities[entity[0]] = entity[1]

                for ent in ents:
                    if ent in entities:
                        cur.execute("UPDATE entities SET count = %s WHERE name = %s AND year = %s;", (ents[ent] + entities[ent], ent, year))
                    else:
                        cur.execute("INSERT INTO entities(name, year, count) VALUES (%s, %s, %s);", (ent, year, ents[ent]))

            cur.execute("UPDATE articles SET processed = true WHERE id IN %s;", (tuple([article[0] for article in articles]),))
