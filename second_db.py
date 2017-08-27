import bs4 as bs
import requests
from urllib.parse import urljoin
import urllib.request
import re
import csv
import psycopg2

path = "/Users/evaverne/Documents/Programming/doineedavisa/CountriesGoogle.csv"
file = open(path, encoding='utf8')
reader = csv.reader(file)

conn_string = "dbname='visachecker' user = 'evaverne'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

droptable = "DROP TABLE test1"
cursor.execute(droptable)
conn.commit()

createtable = "CREATE TABLE test1 (uid serial PRIMARY KEY, country VARCHAR(100) not null)"
cursor.execute(createtable)
conn.commit()

for row in reader: 
	statement = "INSERT INTO test1 (country) VALUES ('"+ row[0] +"') RETURNING uid"

	cursor.execute(statement)
	conn.commit()
	templateid = cursor.fetchone()[0]


