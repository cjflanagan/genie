import pdb
from connection import connection
import csv
import tarfile
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import psycopg2
import shutil
import spacy

url = "ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/"
nlp = spacy.load("en_core_sci_sm")

while True:
    with connection:
        with connection.cursor() as cur:
            cur.execute("""
                SELECT id, filename
                FROM articles
                WHERE processed = false
                ORDER BY published_at
                DESC LIMIT 10;
            """)

            articles = cur.fetchall()
            ents = {}

            for article in articles:
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
                if abstract:
                    abstract = ET.tostring(abstract, method = "text").decode()
                    for ent in nlp(abstract).ents:
                        ents[ent.text.lower()] = ents.get(ent.text.lower(), 0) + 1

            if len(ents):
                entities = {}

                cur.execute("SELECT id, count FROM entities WHERE id IN %s;", (tuple([*ents]),))
                for entity in cur.fetchall():
                    entities[entity[0]] = entity[1]

                for ent in ents:
                    if ent in entities:
                        cur.execute("UPDATE entities SET count = %s WHERE id = %s;", (ents[ent] + entities[ent], ent))
                    else:
                        cur.execute("INSERT INTO entities VALUES (%s, %s);", (ent, ents[ent]))

            cur.execute("UPDATE articles SET processed = true WHERE id IN %s;", (tuple([article[0] for article in articles]),))
