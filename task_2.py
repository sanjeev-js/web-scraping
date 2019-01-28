from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json

imdb_url=("https://www.imdb.com/india/top-rated-indian-movies/")
response=requests.get(imdb_url)
soup=BeautifulSoup(response.content,'html.parser')
data_container=soup.find('div',class_="lister")
table_body=data_container.find("tbody",class_="lister-list")
table_row=table_body.findAll('tr')
list_1=[]

movie_name_list=[]
year_list=[]
rating_list=[]
link_list=[]

for tr in table_row:

	movie_name=tr.find('td',class_="titleColumn").a.get_text()
	movie_name_list.append(movie_name)

	year=tr.find('td',class_="titleColumn").span.get_text()
	year=year.replace("(","").replace(")","")
	year_list.append(year)

	rating=tr.find('td',class_="imdbRating").strong.get_text()
	rating=float(rating)
	rating_list.append(rating)

	url="https://www.imdb.com%26quot%3B/"
	link=tr.find('td',class_="titleColumn").a['href']
	for i in range(len(link)):
		if link[i]!="?":
			url=url+(link[i])
		else:
			link_list.append(url)
			break

all_data={"Position":"","Name":"","Year":"","Rating":"","url":""}
all_data_list=[]

for i in range(len(movie_name_list)):
	all_data["Position"]= i+1
	all_data["Name"]=movie_name_list[i]
	all_data["Year"]=year_list[i]
	all_data["Rating"]=rating_list[i]
	all_data["url"]=link_list[i]
	all_data_list.append(all_data.copy())

def group_by_year(all_data_list):	
	group_by_year_list={}
	for i in sorted(year_list):
		temp=[]
		for j in all_data_list:
			if j["Year"]==i:
				temp.append(j)
		group_by_year_list[i]=temp
	return group_by_year_list
a=group_by_year(all_data_list)
pprint (a)

