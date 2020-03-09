import pdb
from csv import reader
import psycopg2
import datetime

with psycopg2.connect(host = "localhost", port = "5432", database = "genie") as conn:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM articles;")

        with open("files/oa_file_list.csv") as csv_file:
            csv_reader = reader(csv_file)

            i = 0
            for row in csv_reader:
                cur.execute("INSERT INTO articles VALUES (%s, %s, %s, false, %s, %s);",(row[2], row[0], row[3], datetime.datetime.now(), datetime.datetime.now()))
                i+= 1
                print(i)
