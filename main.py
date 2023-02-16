url = "https://www.dailypost.vu/news/communities-upgrade-own-road/article_b97ca4f6-471b-5eae-8066-2a890057ca02.html#tncms-source=article-nav-next"
import requests 

r = requests.get(url)

# print (r.text) 

with open ('article.html', 'w') as file:

    file.write(r.text)
