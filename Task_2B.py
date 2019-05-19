import requests 
from bs4 import BeautifulSoup
import json
import os

if os.path.exists("Box-office.json"):
	with open("Box-office.json", "r") as file:
		data = file.read()
		print (data)
else:

	Imdb_url = "https://www.imdb.com/"
	response = requests.get(Imdb_url)
	a = BeautifulSoup(response.content, "html.parser")
	b = a.find('div', class_= "subNavListContainer")
	uls = b.find_all('ul')
	for j in uls:
		lis=j.find('li')
		if lis.text=="Box Office":
			link = lis.find('a')['href']

	box_office_link = Imdb_url + link

	# Requesting From Box Office

	box_office = requests.get(box_office_link)
	soup = BeautifulSoup(box_office.content, "html.parser")
	c = soup.find('div', class_= "article listo")
	d = c.find('table', class_="chart full-width")
	e = d.find('tbody')
	trs = e.find_all('tr')

	movie_name_list = []
	cast_list = []
	for tr in trs:
		td = tr.find('td', class_="titleColumn")
		g = td.find('a')
		movie_name = (g.text)
		movie_name_list.append(movie_name)
		movie_link = (g['href'])[1:]

		movie_url = Imdb_url+movie_link

		movie_response = requests.get(movie_url)
		temp=[]
		soup1 = BeautifulSoup(movie_response.content, 'html.parser')
		div = soup1.findAll('div', class_ = "see-more")
		for k in div:
			anchor = k.find('a')
			if anchor.text == "See full cast":
				cast_link = anchor['href']
				
				cast_url = Imdb_url+movie_link+'/'+cast_link
				cast_response = requests.get(cast_url)
				soup2 = BeautifulSoup(cast_response.content, "html.parser")
				table = soup2.find('table', class_ = "cast_list")
				tds = table.find_all('td',class_="")
				# print (tds)

				for td in tds:
					ar=td.find('a')
					cast_name = (ar.text).strip()
					temp.append(cast_name)
				cast_list.append(temp)
	# print (cast_list)
	# print (movie_name_list)

	all_details = []

	details = {"MovieName" : "", "Cast": ""}

	for i in range(len(cast_list)):
		details["MovieName"] = movie_name_list[i]
		details["Cast"] = cast_list[i]
		all_details.append(details.copy())
	# pprint (all_details)

	with open ("Box-office.json", "w") as file:
		final = json.dumps(all_details)
		file.write(final)