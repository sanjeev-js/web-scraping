from bs4 import BeautifulSoup
import requests

page  = requests.get("http://questions.menstrupedia.com")
data = BeautifulSoup(page.content, "html.parser")
textContent = []

Questions = data.findAll(class_="question-summary-wrapper")

c=0
for i in Questions:
	c+=1
	Ques = i.find("h2").get_text()
	print(str(c)+". "+str(Ques))
	h = i.find("a")
	print(h["title"]+"\n")
	print("---------------------------------------------------------------------------------------")
			
