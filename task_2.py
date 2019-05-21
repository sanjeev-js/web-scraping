# Importing request// Requests is a Python module that you can use to send all kinds of HTTP requests.
import requests
# Import pprint for pretty look of dictionary.
from pprint import pprint
# imports BeautifulSoup // Beautiful Soup is a Python library for pulling data out of HTML and XML files. 
from bs4 import BeautifulSoup 

# function to scrap top 250 listed Indian movies on imdb.
# http request on the link where top 250listed indian movies. 
r=requests.get("https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in")

# getting text of requested data
page=r.text
# Here I am parsing html content in text
parse=BeautifulSoup(page,"html.parser")
# lister is the class of main div in which a tbody .
lister=parse.find("div",class_="lister")
# tbody is a html tag in there are many td in each tr there is h tag and td tags under which there is movie name.
tbody=lister.find("tbody",class_="lister-list")
j=1
movie_rank=[]
movie_name=[]
movie_year=[]
movie_rating=[]
movie_link=[]
Dictionary_list=[]
# here i am find all tr tag in each tr we have anchor tag , span tag and td tag from here we scraped the data.
trs=tbody.find_all("tr")
# Using loop I am going inside in each tr
for tr in trs:
	# In each tr i am finding td ,span and anchor tag where i am getting movie_name,year,rating,,movie_link respectively
	td=tr.find("td", class_="titleColumn")
	# appending movie_rank data in list named movie_rank
	movie_rank.append(j)
	name=td.find("a").text
	# appending movie_name data in list named movie_name
	movie_name.append(name)
	year=td.find("span").text
	# appending movie_year data in list named movie_year
	movie_year.append(year)
	rating=tr.find("td",class_="ratingColumn imdbRating").text.strip()
	# appending movie_rating data in list named movie_rating
	movie_rating.append(rating)
	link=tr.find("td", class_="titleColumn").a["href"]
	main_link="http://www.imdb.com"+link
	# appending movie_link data in list named movie_link
	movie_link.append(main_link)
	j+=1
# here i using loop on lists that we have made recently and appended data 
for i in range(250):
	# now append all details of one movie in a dictionary
	dic={
    "name": movie_name[i],
    "year": movie_year[i],
    "position": movie_rank[i],
    "rating": movie_rating[i],
    "url": movie_link[i]
  }
  # appending dictionary in Dictionary_list
	Dictionary_list.append(dic)
# pprint(Dictionary_list)

#  Group movie by year

Task2_dic={}
for j in movie_year:
	list_task2=[]
	for k in range(250):
		if j==Dictionary_list[k]["year"]:
			dic2={"name":Dictionary_list[k]["name"],"year":j,
			"position":Dictionary_list[k]["position"],"rating":Dictionary_list[k]["rating"],"url":Dictionary_list[k]["url"]}
			list_task2.append(dic2)
	Task2_dic[j] = list_task2
pprint (Task2_dic)
