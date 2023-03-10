import json
import requests
from bs4 import BeautifulSoup

BASEURL = "https://www.dailypost.vu"
DATAFILE = "data_file.json"


def load_articles():
    with open(DATAFILE, "r") as read_file:
        return json.load(read_file)


def save_articles(articles):
    with open(DATAFILE, "w") as write_file:
        json.dump(articles, write_file)


def fetch(path="/news"):
    response = requests.get(f"{BASEURL}{path}")
    return response.text


def get_card_data(card):
    """creates dictionary of article data from cardpanels"""
    headline = card.article.find("div", class_="card-headline").text.strip()
    lead = card.article.find("div", class_="card-lead").text.strip()
    url = card.article.a["href"]
    return dict(headline=headline, lead=lead, url=url)


def get_images(article):
    images = []  # empty list
    owl_images = article.find_all("img", class_="owl-lazy")
    if len(owl_images) == 0:
        # single image only
        src = article.find("img")["src"]
        try:
            caption = article.find("figcaption").find("p").text.strip()
        except AttributeError:
            caption = None
        images.append(dict(src=src, caption=caption))
    else:
        for item in article.find_all("div", class_="item-container"):
            src = item.find("img")["src"]
            caption = None
            if item.find("div", class_="caption-container").find("p"):
                caption = (
                    item.find("div", class_="caption-container").find("p").text.strip()
                )

            images.append(dict(src=src, caption=caption))
    return images


def get_article_data(article):
    headline = article.h1.text.strip()
    images = get_images(article)
    meta = article.find("div", class_="meta")
    date = meta.time["datetime"]

    author = None
    if meta.find("span", class_="tnt-byline", itemprop="author"):
        author = meta.find("span", class_="tnt-byline", itemprop="author").text.strip()
    paragraphs = article.find("div", id="article-body").find_all("p")

    paragraph_list = []
    for p in paragraphs:
        paragraph_list.append(p.text.strip())

    return dict(
        date=date,
        author=author,
        headline=headline,
        story=paragraph_list,
        images=images,
    )


def main():
    new_articles = []
    articles = load_articles()
    if articles:
        latest_article = max(articles, key=lambda a: a["date"])
    # collect articles from news page
    print("fetching_news")
    html = fetch()
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("div", id="tncms-region-index-primary")
    cardpanels = section.find_all("div", class_="card-panel")
    for card in cardpanels:
        data = get_card_data(card)  # this is where the loop takes from dictionary
        if articles and latest_article["url"] == data["url"]:
            break
        new_articles.append(data)

    for count, article in enumerate(new_articles):
        print(f"fetching {article['headline']}")
        html = fetch(article["url"])
        soup = BeautifulSoup(html, "html.parser")
        data = get_article_data(soup.article)
        article.update(data)

    articles.extend(new_articles)
    save_articles(articles)


if __name__ == "__main__":
    main()
