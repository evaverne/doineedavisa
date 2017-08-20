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
andeverytime = "CREATE TABLE test2 (uid serial PRIMARY KEY, citizenship INTEGER, FOREIGN KEY (citizenship) REFERENCES test (uid), country INTEGER, FOREIGN KEY (country) REFERENCES test1 (uid), requirements VARCHAR(100), comment VARCHAR(300))"

cursor.execute(everytime)
conn.commit()
cursor.execute(andeverytime)
conn.commit()

index = 1		#begin with Afghanistan 
index_for_coun = 0

for item in storage2:
	new_url = urljoin('https://en.wikipedia.org/wiki/', storage2[index])
	print(new_url)
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
	requirement = []
	comment = []

	for group in chunks:
		country0.append(group[0])
		requirement.append(group[1])
		comment.append(group[2])

	country1 = ['\xa0Ivory Coast' if x == "\xa0Côte d'Ivoire" else x for x in country0]
	country = []

	for item in country1: 
		new_item = re.sub('\xa0', '', item)
		country.append(new_item)

	for each in country:
		command1 = "SELECT uid FROM test WHERE citizenship = '{}'".format(final_storage[index])
		cursor.execute(command1)
		conn.commit()
		after_command1 = cursor.fetchone()[0]	#should return the uid of the citizenship
		after = str(after_command1)

		command2 = "INSERT INTO test2 (citizenship) VALUES ({})".format(after)
		cursor.execute(command2)
		conn.commit()	#should put the previous uid into the final table
		#after_command2 = cursor.fetchone()[0]	#do I need to fetch it?

		command3 = "SELECT uid FROM test1 WHERE country = '{}'".format(country[index_for_coun])
		cursor.execute(command3)
		conn.commit()
		after_command3 = cursor.fetchone()[0]
		after3 = str(after_command3)
		print(after3)
		
		# command4 = "INSERT INTO test2 (country) VALUES (%s)"
		
		#after_command3 = cursor.fetchone()[0]	#should return the uid of the country
		
		command4 = "INSERT INTO test2 (country) VALUES ({})".format(after3)
		cursor.execute(command4)
		conn.commit()
		# index_for_coun = (index_for_coun + 1) % len(country)
			#after_command4 = cursor.fetchone()[0]		#do I need to fetch it?
	
	for req in requirement:
		command5 = "INSERT INTO test2(requirements) VALUES (%s)"
		after5 = str(req[index_for_coun])
		cursor.execute(command5, after5)
		conn.commit()
	print(len(comment))
	print(comment)
	for com in comment:
		command6 = "INSERT INTO test2(comment) VALUES (%s)"
		after6 = str(com[index_for_coun])
		cursor.execute(command6, after6)
		conn.commit()

	index = (index + 1) % len(final_storage)
	index_for_coun = (index_for_coun + 1) % len(country)

# number = 1
# command = 'SELECT citizenship FROM test WHERE uid = {}'.format(number)
# cursor.execute(command)
# conn.commit()
# var = cursor.fetchone()[0]



# print(var)




