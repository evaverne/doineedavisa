import requests
import psycopg2 
import re
import csv
from urllib.parse import urljoin
import urllib.request
import bs4 as bs
import logging



#the code below goes through the list of categories with wiki api and creates csv list

main_api = 'https://en.wikipedia.org//w/api.php?action=parse&format=json&page=Category%3AVisa+requirements+by+nationality&prop=links'
json_data = requests.get(main_api).json()
normal_json = json_data['parse']['links']

storage = []
index = 0
print(normal_json)
for item in normal_json:
	example = json_data['parse']['links'][index]['*']
	index = (index + 1) % len(normal_json)
	next_example = json_data['parse']['links'][index]['*']
	storage.append(next_example)

storage0 = []
print(storage)
pattern = re.compile('Visa requirements for ()')
for item in storage:
	if pattern.findall(item):
		storage0.append(item)

storage_zero = []
storage1 = []
final_storage = []

regular = re.compile("Visa requirements for British Overseas ()")
pattern = re.compile('Visa requirements for ()')

for item in storage0: 
	if regular.findall(item):
		storage0.pop()
	else:
		storage_zero.append(item)

for thing in storage_zero:
	if pattern.findall(thing):
		storage1.append(thing)

for thing in storage1:
	new_thing = re.sub('Visa requirements for ', '', thing)
	final_storage.append(new_thing)

csvfile = "/Users/evaverne/Documents/Programming/doineedavisa/Category.csv"
with open(csvfile, 'w', encoding='utf8') as output:
	writer = csv.writer(output)
	for val in final_storage:
		writer.writerow([val])

#the code below takes the data from the csv file and imports it into PostgreSQL table

path = "/Users/evaverne/Documents/Programming/doineedavisa/Category.csv"
file = open(path, encoding='utf8')
reader = csv.reader(file)

conn_string = "dbname='visachecker' user = 'evaverne'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

command_one = "DROP TABLE test"
command_two = "CREATE TABLE test (uid serial PRIMARY KEY, citizenship VARCHAR(200) not null)"
cursor.execute(command_one)
conn.commit()
cursor.execute(command_two)
conn.commit()

for row in reader: 
	statement = "INSERT INTO test (citizenship) VALUES ('"+ row[0] +"') RETURNING uid"

	cursor.execute(statement)
	conn.commit()
	templateid = cursor.fetchone()[0]


# the code below has to take each item, put it into the wiki link and parse it accordingly


# new_url = urljoin('https://en.wikipedia.org/wiki/Visa requirements for Chinese citizens')

# sauce = urllib.request.urlopen(new_url).read()
# soup = bs.BeautifulSoup(sauce, 'lxml')

# start = soup.table.find('td')
# end = soup.find('table').findNext('table').find('td')

# countries = []
# new_countries = []

# while start != end:
# 	countries.append(start.text)
# 	start = start.findNext('td')

# for item in countries: 
# 	new_item = re.sub('[[]\d{1,3}[]]', '', item)
# 	new_countries.append(new_item)

	

# country = []

	
# c_ind = 0
# country.append(new_countries[0])
# for thing in new_countries:
# 	first_el = new_countries[c_ind]
# 	c_ind = (c_ind + 3) % len(new_countries)
# 	next_el = new_countries[c_ind]
# 	country.append(next_el)
# country.pop()




# a = set(country)
# b = set(temporary)
# c = list(a | b)

# list_size = len(c)
# print(len(c))
# for len in range(0,list_size):
#     if (len != list_size-1):
#         sql = ' ('+ "'"+  c[len] + "'"+ ') ,'
#     else:
#         sql = '('+ "'"+  c[len] + "'"+ ')'

# cursor.execute("INSERT into test1 (country) values " + sql)
# conn.commit()

# statement = "SELECT country FROM test1"

# cursor.execute(statement)
# conn.commit()
# operatewithit = [r[0] for r in cursor.fetchall()] 
