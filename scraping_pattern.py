import bs4 as bs
import urllib.request
import pandas as pd
from pandas import DataFrame
import numpy as np

sauce = urllib.request.urlopen('https://en.wikipedia.org/wiki/Visa_requirements_for_Chinese_citizens').read()
soup = bs.BeautifulSoup(sauce, 'lxml')

table = soup.find('table')
table_rows = table.find_all('td')

for item in table_rows:
	a1 = item.find_all('a')
	row = [i.text for i in a1]

print(row)



#dfs = pd.read_html('https://en.wikipedia.org/wiki/Visa_requirements_for_Australian_citizens', header=0)
#print(dfs)

#australia = dfs.astype

#dfs.to_csv('Australia.csvdf.to_excel')
