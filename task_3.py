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
	year_list.append(int(year))

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

a=min(year_list)
b=a%10
start_decade=a-b
till=start_decade+9

def group_by_decade(all_data_list)
	group_by_decade_list=[]
	group_by_decade_dict={}
	while (till<=max(year_list)):
		temp=[]
		for i in all_data_list:
			if int (i["Year"])>=start_decade and int (i["Year"])<=till:
				temp.append(i.copy())
		group_by_decade_dict[start_decade]=temp
		temp=[]
		group_by_decade_list.append(group_by_decade_dict.copy())
		start_decade+=10
		till+=10
		return group_by_decade_list
pprint(group_by_decade_list(all_data_list))	