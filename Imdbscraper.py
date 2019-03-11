from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json
import os 

# imdb_url=("https://www.imdb.com/india/top-rated-indian-movies/")
# response=requests.get(imdb_url)
# soup=BeautifulSoup(response.content,'html.parser')
# # all_data={"Position":,"Name":,"Year":,"Rating":,"url":}
# data_container=soup.find('div',class_="lister")
# table_body=data_container.find("tbody",class_="lister-list")
# table_row=table_body.findAll('tr')

# movie_name_list=[]
# year_list=[]
# rating_list=[]
# url_list=[]

# for tr in table_row:
	
# 	movie_name=tr.find('td',class_="titleColumn").a.get_text()
# 	movie_name_list.append(movie_name)

# 	year=tr.find('td',class_="titleColumn").span.get_text()
# 	year=year.replace("(","").replace(")","")
# 	year_list.append(year)

# 	rating=tr.find('td',class_="imdbRating").strong.get_text()
# 	rating=float(rating)
# 	rating_list.append(rating)

# 	url="https://www.imdb.com"
# 	link=tr.find('td',class_="titleColumn").a['href']
# 	for i in link:
# 		if i!='?':
# 			url+=i
# 		else:
# 			break
# 	url_list.append(url)

# def scrape_top_list(movie_name_list,year_list,rating_list,url_list):
	
# 	all_details=[]
# 	dis={"Position":'',"movie_name":'',"year":'',"rating":'',"url":''}
# 	for i in range(len(movie_name_list)):
# 		dis["Position"]=i+1
# 		dis["movie_name"]=movie_name_list[i]
# 		dis["year"]=year_list[i]
# 		dis["rating"]=rating_list[i]
# 		dis["url"]=url_list[i]
# 		all_details.append(dis.copy())
# 	return all_details
# movies=scrape_top_list(movie_name_list,year_list,rating_list,url_list)
	
# def movies_by_year(all_details):
# 	final_dis={}
# 	for year in sorted(year_list):
# 		temp=[]
# 		for dis in all_details:
# 			if dis["year"]==year:
# 				temp.append(dis)
# 		final_dis[year]=temp

# 	return final_dis

# # pprint(movies_year)


# '''Task no three........'''

# ''''''

file=open('url_list.json')
temp=file.read()
url_list=json.loads(temp)

##### task 12 (find the movies cast details)
def get_movies_cast(movie_url):
	list=[]
	dis={}
	response=requests.get(movie_url)
	soup=BeautifulSoup(response.content,'html.parser')
	cast_details = soup.find('table', class_="cast_list")
	name_of_actor=cast_details.find_all('td', class_='')
	for i in name_of_actor:
		name=i.get_text().strip()
		imdb_id=''
		for j in i.a['href'][6:]:
			if j != '/':
				imdb_id+=j
			else:
				break

		dis['imdb_id']=imdb_id
		dis["name"]=name
		list.append(dis.copy())
	return list


#### Task 4(scrap the movies all detail like name, runtiem, produser, langauage etc.)
### 8 (make the cache to save our time and internet to request for the same data again and again)
### 9(slow down the speed for request on the server) .
def scrap_movie_details(movie_url):
	#task 8 ....
	movie_id_is=''
	for i in movie_url[27:]:
		if i !='/':
			movie_id_is+=i
		else:
			break
	file_name=movie_id_is+'.json'
	if os.path.exists('./'+file_name):
		f=open('./'+file_name)
		temp=f.read()
		data=json.loads(temp)
		f.close()
		
		return data
	else:
		response=requests.get(movie_url)
		soup=BeautifulSoup(response.content,'html.parser')

	##here we will find the name of movei first.
		movie_name=''
		title_wrapper=soup.find('div', class_="title_wrapper")
		name_of_movie=soup.find('div',class_="title_wrapper").h1.get_text()
		for i in name_of_movie:
			if i.isalpha():
				movie_name+=i
			else:
				break

	### Here we fine the rest things like runtime and gener and more.
		sub_div=title_wrapper.find('div', class_="subtext")
		runtime= sub_div.find('time').get_text().strip()
		runtime_hours= int(runtime[0])
		if 'min' in runtime:
			runtime_min=int(runtime[3:].strip('min'))
			runtime_in_min=runtime_hours*60 + runtime_min
		else:
			runtime_in_min=runtime_hours*60

		gener= sub_div.find_all('a')
		gener_list=[]
		for i in range(len(gener)-1):
			gener_list.append(gener[i].get_text())

	### Here we will find the main things like how to find the summary and directore name.
		summary=soup.find('div', class_="plot_summary")
		summary_text=summary.find('div', class_="summary_text").get_text().strip()
		directore=summary.find('div', class_="credit_summary_item")
		directore_list=directore.find_all('a')
		directores=[i.get_text() for i in directore_list]

	### Here I am getting the poster url.
		poster_image_url=soup.find('div', class_="poster").a['href']
		movie_poster= "https://www.imdb.com"+poster_image_url

	### Now we will find the extra ditails.
		extra_details = soup.find('div', attrs={"class":"article","id":"titleDetails"})
		div_list = extra_details.findAll('div')
		for div in div_list:
			tag4= div.findAll('h4')
			for text in tag4:
				if 'Language:' in text:
					tag_anchore=div.find_all('a')
					movie_languages=[i.get_text() for i in tag_anchore]
				elif 'Country:' in text:
					tag_anchore=div.find_all('a')
					country_name=' '.join([i.get_text() for i in tag_anchore])

	### Here we are making the dicstionary as all data we will store in it.
		movie_data={}

		movie_data["name"]=movie_name
		movie_data["directore"]=directores
		movie_data["country"]=country_name
		movie_data["language"]=movie_languages
		movie_data["poster_url"]=movie_poster
		movie_data["bio"]=summary_text
		movie_data["runtime"]=runtime_in_min
		movie_data["gener"]=gener_list

		details_cast={}
		details_cast['local_details']=movie_data
		details_cast['cast']=get_movies_cast(movie_url)

		s=json.dumps(details_cast)
		with open('./'+file_name, "w+") as file:
			file.write(s)

		return details_cast

## task no 5 in this task wi will make a json for of all movies details.

def get_list_of_movies_details(url_list):
	movie_details=[]
	for i in url_list:
		temp=scrap_movie_details(i)
		movie_details.append(temp)
	return movie_details

movies_details=get_list_of_movies_details(url_list)
# pprint(movies_details)

### Task 6
#in this task we will analys movies based on the languages.

def analys_movies_language(movies_details):
	analys_dis={}
	for dis in movies_details:
		for language in	dis['local_details']['language']:
			if language in analys_dis:
				analys_dis[language]+=1
			else:
				analys_dis[language]=1
	return analys_dis
# pprint(analys_movies_language(movies_details))


### Task 7
def analys_movies_director(movies_details):
	analys_dis={}
	for dis in movies_details:
		for directore in dis['local_details']['directore']:
			if directore in analys_dis:
				analys_dis[directore]+=1
			else:
				analys_dis[directore]=1
	return analys_dis
# pprint(analys_movies_director(movies_details))





### Task 10(analys the movie details by the director and language both)
def analys_director_language(movies_details):
	analys_dis={}
	for dis in movies_details:
		analys_dis_language={}
		for directore in dis['local_details']['directore']:
			for language in	dis['local_details']['language']:
				if directore in analys_dis:
					if language in analys_dis[directore]:
						analys_dis[directore][language]+=1
					else:
						analys_dis[directore][language]=1
				else:
					if language in analys_dis_language:
						analys_dis_language[language]+=1
					else:
						analys_dis_language[language]=1
					analys_dis[directore]=analys_dis_language

	return analys_dis
pprint(analys_director_language(movies_details))


####  Task 11(analys movies by gener)
def analys_movies_gener(movies_details):
	analys_dis={}
	for dis in movies_details:
		for gener in dis['local_details']['gener']:
			if gener in analys_dis:
				analys_dis[gener]+=1
			else:
				analys_dis[gener]=1
	return analys_dis 
# pprint(analys_movies_gener(movies_details))


def get_cast_from_cache(movies_details):
	list=[]
	for dis in movies_details:
		list.append(dis['cast'])
	return list
# pprint(get_cast_from_cache(movies_details))


#### task 14(main main mian mian kai keu ab to bas moj hai.)
def get_often_pairs(cast_details):
	dis_pairs={}
	for list1 in cast_details:
		for i in range(2):
			actor_id=list1[i]['imdb_id']
			if actor_id not in dis_pairs:				
				dis_2={}
				dis_2["name"]=list1[i]['name']
				dis_pairs[actor_id]=dis_2
				temp=[]
				for j in list1[i+1:]:
					if j not in temp:
						j['num_movie']=1
						temp.append(j)
					dis_2['frequent_co-actore']=temp
			else:
				for j in list1[i+1:]:
					if j in dis_2['frequent_co-actore']:
						j['num_movie']+=1
	return dis_pairs
# often_pairs=get_often_pairs(get_cast_from_cache(movies_details))
# print(often_pairs)


### Task 15

def get_frequent_actore(cast_details):
	dis_pairs={}
	for list1 in cast_details:
		for i in list1:
			actor_id=i['imdb_id']
			if actor_id not in dis_pairs:				
				dis_2={}
				dis_2["name"]=i['name']
				dis_2['num_movie']=1
				dis_pairs[actor_id]=dis_2
			else:
				dis_pairs[actor_id]['num_movie']+=1
	actore_re={}			
	for i, j in dis_pairs.items():
		if j['num_movie']>1:
			actore_re[i]=j

	return actore_re
# pprint(get_frequent_actore(get_cast_from_cache(movies_details)))

# s=json.dumps(url_list)
# with open('url_list.json', "w") as f:
# 	f.write(st
