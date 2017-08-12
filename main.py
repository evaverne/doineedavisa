import bs4 as bs
import urllib.request
import numpy as np
import requests
import re
import unicodedata
from flask import Flask, render_template, request
import csv
import dis
import logging
from urllib.parse import urljoin

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

# new_url = urljoin('https://en.wikipedia.org/wiki/', example)
# print(new_url)

app = Flask(__name__)
@app.route('/visaanswer', methods = ["GET", "POST"])
def visaanswer():
	if request.method == "POST":
		country_one = request.form['countr']
		new_url = urljoin('https://en.wikipedia.org/wiki/', country_one) #starting from here
		app.logger.info(country_one)
		return render_template('webversion2.html', countries = ["One", "Two", "Three"])
	return render_template('webversion2.html', abstract = final_storage)


sauce = urllib.request.urlopen('https://en.wikipedia.org/wiki/Visa_requirements_for_Chinese_citizens').read()
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

#print(new_countries)

country = []
requirement = []
comment = []

c_ind = 0
country.append(new_countries[0])

for thing in new_countries:
	first_el = new_countries[c_ind]
	c_ind = (c_ind + 3) % len(new_countries)
	next_el = new_countries[c_ind]
	country.append(next_el)
country.pop()

req_ind = 1
requirement.append(new_countries[1])

for thing in new_countries:
	first_el = new_countries[req_ind]
	req_ind = (req_ind + 3) % len(new_countries)   #why % len?
	next_el = new_countries[req_ind]
	requirement.append(next_el)
requirement.pop()

com_ind = 2
comment.append(new_countries[2])

for thing in new_countries:
	first_el = new_countries[com_ind]
	com_ind = (com_ind + 3) % len(new_countries)
	next_el = new_countries[com_ind]
	comment.append(next_el)
comment.pop()


print(country[10])
print(requirement[10])
print(comment[10])


if __name__ == "__main__":
	app.run(debug=True)
