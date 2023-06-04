import os
import pandas as pd

import utils

from config import radicals_fn

if not os.path.isfile(radicals_fn):
	data = []
	link = 'https://www.japandict.com/radicals'
	if soup := utils.get_soup(link):
		tr_s = soup.findAll('tr')
		for tr in tr_s:
			if number_span := tr.find('span', attrs={'class': 'd-none d-lg-inline'}):
				row = tr.findAll('td', attrs={'class': 'p-1 p-lg-3'})
				row_values = []
				for cell in row:
					row_values.append(cell.text)
				data.append(row_values)

	df = pd.DataFrame(data[1:], columns=['radical', 'other_form', 'stroke_count', 'tags', 'meaning'])
	df.to_excel(radicals_fn)
else:
	print('Radicals file already exist.')