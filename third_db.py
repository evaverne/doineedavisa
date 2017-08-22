import bs4 as bs
import requests
from urllib.parse import urljoin
import urllib.request
import re
import csv
import psycopg2

conn_string = "dbname='visachecker' user = 'evaverne'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

main_api = 'https://en.wikipedia.org//w/api.php?action=parse&format=json&page=Category%3AVisa+requirements+by+nationality&prop=links'
json_data = requests.get(main_api).json()
normal_json = json_data['parse']['links']

storage = []
index = 0

for item in normal_json:
	example = json_data['parse']['links'][index]['*']
	index = (index + 1) % len(normal_json)
	next_example = json_data['parse']['links'][index]['*']
	storage.append(next_example)

storage2 = []

pattern = re.compile('Visa requirements for ()')
for item in storage:
	if pattern.findall(item):
		storage2.append(item)

final_storage = []

for thing in storage2:
	new_thing = re.sub('Visa requirements for ', '', thing)
	final_storage.append(new_thing)

#the code below creates the DB in PostgreSQL and prepares data for the import

everytime = "DROP TABLE test2"
andeverytime = "CREATE TABLE test2 (uid serial PRIMARY KEY, citizenship INTEGER NOT NULL, FOREIGN KEY (citizenship) REFERENCES test (uid), country VARCHAR(100), requirements VARCHAR(100), comment VARCHAR(500))"

cursor.execute(everytime)
conn.commit()
cursor.execute(andeverytime)
conn.commit()

index = 1		#begin with Afghanistan 
index_for_coun = 0

for item in storage2:
	new_url = urljoin('https://en.wikipedia.org/wiki/', storage2[index])
	sauce = urllib.request.urlopen(new_url).read()
	soup = bs.BeautifulSoup(sauce, 'lxml')

	start = soup.table.find('td')
	end = soup.find('table').findNext('table').find('td')

	countries = []
	new_countries = []

	while start != end:
		countries.append(start.text)
		start = start.findNext('td')

	for item in countries: 
		new_item = re.sub('[[]\d{1,3}[]]', '', item)
		new_countries.append(new_item)
	
	chunks = [new_countries[x:x+3] for x in range(0, len(new_countries), 3)]

	country0 = []
	requirement0 = []
	comment = []
	country = []
	
	for group in chunks:
		if len(group) == 3:
			country0.append(group[0])
			requirement0.append(group[1])
			comment.append(group[2])
		else:
			chunks.pop()

	country1 = ['\xa0Ivory Coast' if x == "\xa0Côte d'Ivoire" or x == "\xa0Cote d'Ivoire" or x == "Cote d'Ivoire !\xa0Côte d'Ivoire" else x for x in country0]
	requirement = ["Visitor''s" if x == "Visitor's" else x for x in requirement0]

	for item in country1: 
		new_item = re.sub('\xa0', '', item)
		country.append(new_item)

	for each in country:
			# command = "SELECT uid FROM test WHERE citizenship = '{}'".format(final_storage[index])
			cursor.execute("SELECT uid FROM test WHERE citizenship = '{}'".format(final_storage[index]))
			conn.commit()
			after_command = cursor.fetchone()[0]	#should return the uid of the citizenship
			after = str(after_command)
		
			# сommand1 = "SELECT uid FROM test1 WHERE country = '{}'".format(country[index_for_coun])
			cursor.execute("SELECT uid FROM test1 WHERE country LIKE '{}'".format(country[index_for_coun]))
			conn.commit()
			after_command1 = cursor.fetchone()
			after1 = str(after_command1)

			command2 = "INSERT INTO test2 (citizenship, country, requirements, comment) VALUES (%s, %s, %s, %s)"
			alltheshit = (after, after1, requirement[index_for_coun], comment[index_for_coun])
			cursor.execute(command2, alltheshit)
			conn.commit()	#should put the previous uid into the final table
			index_for_coun = (index_for_coun + 1) % len(country)

	index = (index + 1) % len(final_storage)


