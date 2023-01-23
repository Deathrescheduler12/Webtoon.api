import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os

from win10toast_click import ToastNotifier
import webbrowser as webb
import os

CLASS_ = "daily_section _list_"

toast = ToastNotifier()

class Webtoon:
    def __init__(self, **info):

        self.url = info["Url"]
        self.author = info["Author"]
        self.name = info["Name"]
        self.image: Image = info["Img"]

    def __repr__(self):
        return f"<Toon name= '{self.name}' author= '{self.author}' url= '{self.url}'>"
class Image:
    def __init__(self, name, url, *, format):
        self.name = name
        self.url = url

        self.path = os.path.join(os.getcwd(), "images")

        
class Daily:
    def __init__(self, genre):
        self.genre = genre
        self.toons = []

        self.url = "https://www.webtoons.com/en/dailySchedule"
    def __repr__(self) -> str:
        repre = self.__get()

        return str(self.toons)
    def __getitem__(self, index):
        self.__get()

        if isinstance(index, int):
            return self.toons[index]
    def __get(self):
        resp = requests.get(self.url)

        soup = bs(resp.text, "html.parser")

        day = datetime.now().strftime("%A")
        toons = soup.find("div", class_=CLASS_ + day.upper())

        s = toons.ul.find_all("a")
        s = self.__filter(s)

        return s
    def __filter(self, a):
        n = []
        for x in a:
            gen = x.find("p", class_="genre").text
            if self.genre.lower() == gen.lower():
                info = Webtoon(**self.__inform(x))
                self.toons.append(info)
        
    def __inform(self, t):
        name = t.find("p", class_="subj").text
        url = t["href"]
        author = t.find("p", class_="author").text
        img = t.find("img")["src"]

        return {"Name" : name, "Author" : author, "Url" : url, "Img" : Image(name, img, format="png")}

