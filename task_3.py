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
pprint(Dictionary_list)



Task3_dic={}
j='(1971)'
for i in movie_year:  # to find out the minimum year of movies and maximm year of movies.
	if int(i[1:-1])>int(j[1:-1]):
		j=i
# print (j)

for i in (range(1950,2020,10)):
	list_task3=[]
	for j in range(i,i+10):
		for k in Dictionary_list:
			if int(k["year"][1:-1])==j:
				dic={
					"name": k["name"],
					"year": k["year"],
					# "position": k["position"],
					"rating": k["rating"]
					# "url": k["url"]
					}
				list_task3.append(dic)

	Task3_dic[i]=list_task3
pprint (Task3_dic)
