import pdb
from csv import reader
from connection import connection
import datetime

with connection:
    with connection.cursor() as cur:
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
                    cur.execute("INSERT INTO articles VALUES (%s, %s, %s, false, %s, %s);",(row[2], row[0], row[3], str(datetime.datetime.now()), str(datetime.datetime.now())))
                    i+= 1
                    print(i)
