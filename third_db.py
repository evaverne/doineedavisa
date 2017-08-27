import bs4 as bs
import requests
from urllib.parse import urljoin
import urllib.request
import re
import csv
import psycopg2
import pdb
 
conn_string = "dbname='visachecker' user = 'evaverne'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

main_api = 'https://en.wikipedia.org//w/api.php?action=parse&format=json&page=Category%3AVisa+requirements+by+nationality&prop=links'
json_data = requests.get(main_api).json()
normal_json = json_data['parse']['links']

storage = []
index_here = 0

for item in normal_json:
	example = json_data['parse']['links'][index_here]['*']
	index_here = (index_here + 1) % len(normal_json)
	next_example = json_data['parse']['links'][index_here]['*']
	storage.append(next_example)	


storage_zero = []
regular = re.compile("Visa requirements for British Overseas ()")
pattern = re.compile('Visa requirements for ()')
storage0 = []

# answer the question: why couldn't you make one loop?
for item in storage: 
	if regular.findall(item):
		storage.pop()
	else:
		storage_zero.append(item)

for thing in storage_zero:
	if pattern.findall(thing):
		storage0.append(thing)

for damn in storage0:
		if damn == "Visa requirements for European Union citizens":
			storage0.remove("Visa requirements for European Union citizens")

final_storage = []

for thing in storage0:
	new_thing = re.sub('Visa requirements for ', '', thing)
	final_storage.append(new_thing)

#the code below creates the DB in PostgreSQL and prepares data for the import

everytime = "DROP TABLE test2"
andeverytime = "CREATE TABLE test2 (uid serial PRIMARY KEY, citizenship INTEGER NOT NULL, FOREIGN KEY (citizenship) REFERENCES test (uid), country VARCHAR(300), requirements VARCHAR(250), comment VARCHAR(1200))"

cursor.execute(everytime)
conn.commit()
cursor.execute(andeverytime)
conn.commit()

index = 0		#begin with Afghanistan 
index_for_coun = 0
#print(storage2[23])
storage2 = ['Visa_requirements_for_Bosnia_and_Herzegovina_citizens' if x == 'Visa requirements for Bosnia and Herzegovina citizens' else x for x in storage0]
storage3 = ['Visa_requirements_for_Chinese_citizens_of_Hong_Kong' if x == 'Visa requirements for Chinese citizens of Hong Kong' else x for x in storage2]
storage4 = ['Visa_requirements_for_Haitian_citizens' if x == 'Visa requirements for Haitian citizens' else x for x in storage3]
storage5 = ['Visa_requirements_for_Honduran_citizens' if x == 'Visa requirements for Honduran citizens' else x for x in storage4]
storage6 = ['Visa_requirements_for_Hungarian_citizens' if x == 'Visa requirements for Hungarian citizens' else x for x in storage5]
storage7 = ['Visa requirements for Monegasque citizens' if x == 'Visa requirements for Monégasque citizens' else x for x in storage6]

for item in storage0:
	#country_get = final_storage[index]		#later this will be used to request.form[] from the user's input
	country_one = storage7[index]
	#country_one = 'Visa requirements for Turkish citizens'
	print(country_one)
	new_url = urljoin('https://en.wikipedia.org/wiki/', country_one)
	sauce = urllib.request.urlopen(new_url).read()
	soup = bs.BeautifulSoup(sauce, 'lxml')

	if country_one == 'Visa requirements for British citizens':
		start = soup.find('table').findNext('table').find('td')
		end = soup.find('table').findNext('table').findNext('table').find('td')
	else:
		start = soup.table.find('td')
		end = soup.find('table').findNext('table').find('td')

	countries = []
	new_countries0 = []

	while start != end:
		countries.append(start.text)
		start = start.findNext('td')

	for item in countries: 
		new_item = re.sub('[[]\d{1,3}[]]', '', item)
		new_countries0.append(new_item)

	# Syntax Loop. the following block removes troubled strings with damn commas and unecessary spaces

	new_countries = ['' if x == '*Available at Hamad International Airport. eVisa is also available.' or x == '\n\nAvailable at Hamad International Airport.\neVisa is also available.\n\n' else x for x in new_countries0]

	# Irish Loop. Fucking Irish Table is a headache. The following loop deals with the Freedom of Movement
	# column in the table. Like it only exists for Irish People...
	

	if country_one == 'Visa requirements for Irish citizens' or country_one == 'Visa requirements for British citizens':
		for thing in new_countries:
			if thing == '\nFreedom of movement (DK)\n':
				pos = new_countries.index('\nFreedom of movement (DK)\n')
				new_countries[pos:pos+1] = ('Freedom of movement', '')
			elif thing == '\nFreedom of movement\n':
				pos = new_countries.index('\nFreedom of movement\n')
				new_countries[pos:pos+1] = ('Freedom of movement', '')
			elif thing == '\nFreedom of movement (in Constituent countries)\n':
				pos = new_countries.index('\nFreedom of movement (in Constituent countries)\n')
				new_countries[pos:pos+1] = ('Freedom of movement', '')
			elif thing == '\nFreedom of movement (European Netherlands)\n':
				pos = new_countries.index('\nFreedom of movement (European Netherlands)\n')
				new_countries[pos:pos+1] = ('Freedom of movement', '')


	for this in new_countries:
		if this == "Free Visitor's Permit on arrival with valid U.S. visa":
			new_countries.remove("Free Visitor's Permit on arrival with valid U.S. visa")
		elif this == "Visa free for holders of valid U.S. visa or Canada visa":
			new_countries.remove("Visa free for holders of valid U.S. visa or Canada visa")

	# 	elif this == "Visitors holding an 'entry authorisation' letter can pick up a visa on arrival.":
	# 		new_countries.remove("Visitors holding an 'entry authorisation' letter can pick up a visa on arrival.")
	# print(new_countries)

	# Chunk Loop. The following code manages the exceptions of the tables with 4 rows in the table

	if country_one == 'Visa requirements for Canadian citizens' or \
	country_one == 'Visa requirements for British Nationals (Overseas)' or \
	country_one == 'Visa requirements for British citizens' or \
	country_one == 'Visa requirements for French citizens' or \
	country_one == 'Visa requirements for Cuban citizens' or \
	country_one == 'Visa requirements for Jordanian citizens' or \
	country_one == 'Visa requirements for Macedonian citizens' or \
	country_one == 'Visa requirements for Montenegrin citizens' or \
	country_one == 'Visa requirements for Portuguese citizens' or \
	country_one == 'Visa requirements for Saint Kitts and Nevis citizens' or \
	country_one == 'Visa requirements for Serbian citizens' or \
	country_one == 'Visa requirements for Singaporean citizens' or \
	country_one == 'Visa requirements for South African citizens' or \
	country_one == 'Visa requirements for Spanish citizens' or \
	country_one == 'Visa requirements for United States citizens' or \
	country_one == 'Visa requirements for Venezuelan citizens':
		chunks = [new_countries[x:x+4] for x in range(0, len(new_countries), 4)]
	elif country_one == 'Visa requirements for Irish citizens':
		chunks = [new_countries[x:x+5] for x in range(0, len(new_countries), 5)]
	else:
		chunks = [new_countries[x:x+3] for x in range(0, len(new_countries), 3)]

	#I am goint to call it British Loop. So British Loop divides the list into necessary groups.

	country0 = []
	requirement0 = []
	comment = []

	print(chunks)
	for group in chunks:
		if country_one == 'Visa requirements for Lebanese citizens' or \
		country_one == 'Visa requirements for Northern Cypriot citizens' or \
		country_one == 'Visa requirements for Turkmen citizens' or \
		country_one == 'Visa requirements for Turkish citizens':
			chunks.pop()
		elif len(group) == 3:
			country0.append(group[0])
			requirement0.append(group[1])
			comment.append(group[2])
		elif len(group) == 4:
			del group[3]
			country0.append(group[0])
			requirement0.append(group[1])
			comment.append(group[2])
		elif len(group) == 5:
			del group [3]
			del group[3]
			country0.append(group[0])
			requirement0.append(group[1])
			comment.append(group[2])
		else:
			chunks.pop()  #where there's no table at all for instance

	

	print(comment)

	#the code below helps to deal with some minor exceptions 

	country1 = ['\xa0Ivory Coast' if x == "\xa0Côte d'Ivoire" or x == "\xa0Cote d'Ivoire" or x == "Cote d'Ivoire !\xa0Côte d'Ivoire" or x == "Ivory Coast !\xa0Ivory Coast" else x for x in country0]
	requirement1 = ["Visa on arrival" if x == "Visa on arrival !Visitor's Permit on arrival" else x for x in requirement0]
	requirement = ['' if x == "Visa waiver for UK 'C' visa holders until October 2016. Entry permitted only if first point of entry to the Common Travel Area is in the UK." else x for x in requirement1]
	country2 = ['\xa0France' if x == "\xa0France and territories" else x for x in country1]
	country3 = ['\xa0New Zealand' if x == "\xa0New Zealand and territories" else x for x in country2]
	country4 = ['\xa0United Kingdom' if x == "\xa0United Kingdom\nexcluding some Overseas territories" else x for x in country3]
	country5 = ['\xa0United States' if x == "\xa0United States and territories" else x for x in country4]
	country6 = ['\xa0Australia' if x == "\xa0Australia and territories" or x == "\xa0Australia and external territories" else x for x in country5]
	country7 = ['\xa0Denmark' if x == "\xa0Denmark and territories" else x for x in country6]
	country8 = ['\xa0Netherlands' if x == "\xa0Netherlands and territories" else x for x in country7]
	country9 = ['\xa0Nepal' if x == '\xa0\xa0\xa0Nepal' else x for x in country8]
	
	country = []

	for item in country9: 
		new_item = re.sub('\xa0', '', item)
		country.append(new_item)

	#delete if it's not needed
	# for exclud in country: 
	# 	if exclud == "excluding some Overseas territories":
	# 		country.remove("excluding some Overseas territories")
	print(country)
	#print(final_storage)

	# Final Loop puts available data into the Data Base. 
	for each in country:
			cursor.execute("SELECT uid FROM test WHERE citizenship = '{}'".format(final_storage[index]))
			conn.commit()
			after_command = cursor.fetchone()[0]	#should return the uid of the citizenship
			after = str(after_command)
		
			cursor.execute("SELECT uid FROM test1 WHERE country = '{}'".format(country[index_for_coun]))
			conn.commit()
			after_command1 = cursor.fetchone()[0]
			after1 = str(after_command1)

			command2 = "INSERT INTO test2 (citizenship, country, requirements, comment) VALUES (%s, %s, %s, %s)"
			alltheshit = (after, after1, requirement[index_for_coun], comment[index_for_coun])
			cursor.execute(command2, alltheshit)
			conn.commit()	#should put the previous uid into the final table
			index_for_coun = (index_for_coun + 1) % len(country)

	index = (index + 1) % len(final_storage)

# I've got million problems with it: 
# 1) Why the citizenship column returns brackets and comma with the number? How to get rid of it?
# 2) Why some of the countries are missing? But do exist in the wiki table? what are these misterious lands?
# 3) 	
