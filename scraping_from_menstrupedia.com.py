from bs4 import BeautifulSoup
import requests

page  = requests.get("http://questions.menstrupedia.com")
data = BeautifulSoup(page.content, "html.parser")
textContent = []

Ques = data.findAll(class_="question-summary-wrapper")

c=0
for i in Ques:
	c+=1
	Q = i.find("h2").get_text()
	print(str(c)+". "+str(Q))
	h = i.find("a")
	print(h["title"]+"\n")
	print("---------------------------------------------------------------------------------------")
			