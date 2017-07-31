import bs4 as bs
import urllib.request
import pandas as pd
from pandas import DataFrame
import numpy as np

wiki = urllib.request.urlopen('https://en.wikipedia.org/wiki/Visa_requirements_for_Australian_citizens').read()
soup = bs.BeautifulSoup(wiki, 'lxml')

table = soup.find('table')
table_rows = table.find_all('tr')


for item in table_rows:
	td = item.find_all('td')
	row = [i.text for i in td]
	print(row)

#for it in row:
#	it = row[0]
#	oo = it.replace("\\xaO", " ")
	#print(oo)






