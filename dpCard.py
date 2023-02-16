url = "https://www.dailypost.vu/news/"
import requests

r = requests.get(url)

with open ('dpCards.html', 'w') as file:

    file.write(r.text)