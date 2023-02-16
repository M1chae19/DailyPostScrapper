from bs4 import BeautifulSoup

file = "dpCards.html"
with open(file, 'r') as f:
    webpage = f.read()


#dictionary
def get_data(card):
    """function creates dictionary of article data from cardpanels"""
    headline = card.article.find("div", class_="card-headline").text.strip()
    lead = card.article.find("div", class_="card-lead").text.strip()
    url = card.article.a["href"] 
    return dict( headline=headline, lead=lead, url =url)
#
soup = BeautifulSoup (webpage, "html.parser")
section = soup.find("div", id="tncms-region-index-primary")
cardpanels = section.find_all("div", class_="card-panel")
news_stories =[]

#loop
for card in cardpanels:
    data = get_data (card) # this is where the loop takes from dictionary
    news_stories.append(data)

print (news_stories)




   
