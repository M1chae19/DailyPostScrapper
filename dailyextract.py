from bs4 import  BeautifulSoup

file = "article.html"
with open(file, 'r') as f:
    webpage = f.read()

soup = BeautifulSoup (webpage)



def get_images(article):
    images = [] #empty list
    owl_images = article.find_all("img",class_='owl-lazy')
    if len(owl_images)== 0:
        #single image only
        src = article .find ("img")["src"]
        caption = article.find("figcaption").find("p").text.strip()
        images.append(dict(src=src, caption=caption))

    else:
        for item in article.find_all("div", class_="item-container"):
            src = item.find ("img")["src"]
            caption = item.find ("div",class_="caption-container").find("p").text.strip()
            images.append(dict(src=src, caption=caption))
    return images





article = soup.article
headline = article.h1.text.strip()
images = get_images(article)
meta = article.find( "div", class_="meta")
date = meta.time ["datetime"]
author = meta.find("span",class_="tnt-byline", itemprop="author").text.strip()
paragraphs = article.find("div",id= "article-body").find_all ("p")

paragraph_list = []
for p in paragraphs:
    paragraph_list.append (p.text.strip())

data = dict(
    date = date,
    author = author,
    headline =headline,
    story =paragraph_list,
    images=images,    

)
print(data)


