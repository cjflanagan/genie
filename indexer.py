import pdb
from csv import reader
import psycopg2
import datetime

with psycopg2.connect(host = "localhost", port = "5432", database = "genie") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM articles;")
        articles = cur.fetchall()
        ids = set()
        for article in articles:
            ids.add(article[0])

        with open("files/oa_file_list.csv") as csv_file:
            csv_reader = reader(csv_file)

            i = 0
            for row in csv_reader:
                if not row[2] in ids:
                    cur.execute("INSERT INTO articles VALUES (%s, %s, %s, false, %s, %s);",(row[2], row[0], row[3], datetime.datetime.now(), datetime.datetime.now()))
                    i+= 1
                    print(i)
