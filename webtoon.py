import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os

import webbrowser as webb
import os

from errors import NO_EMPTY_TOON as no

CLASS_ = "daily_section _list_"

class Toons:
    def __init__(self, search):
        self.items = []
        if search:
            self.key = search
            self.search()

    def __getattr__(self, __name):
        s = ["url", "author", "name", "image", "key"]

        for x in s:
            if __name.lower() == x:
                return super(Toons, self).__getattribute__(__name.lower())
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Toons):
            return self.items == __o.items
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.items[index]
        elif isinstance(index, slice):
            return self.items[index]
    def search(self):
        base = "https://www.webtoons.com/en"

        resp = requests.get(base + "/search?keyword=" + self.key)

        soup = bs(resp.text, "html.parser")
        
        card_list = soup.find("h3", class_="search_result") \
        .find_next_sibling("ul", class_="card_lst")

        founds = card_list.find_all("li")

        for found in founds:
            info = found.find("div", class_="info")
            
            name = info.find("p", class_="subj").text
            author = info.find("p", class_="author").text
            url = base + "/action" + card_list.find("a", class_="card_item")["href"]

            self.items.append(Toon(Name = name, Author = author, Url = url))
    def __repr__(self):
        return f"Results={str(self.items)}"
class Image:
    def __init__(self, name, content, *, format):
        self.name = name
        self.content = content

        self.path = os.path.join(os.getcwd(), "images")

class Toon:
    def __init__(self, **info):
        if info:
            self.url = info["Url"]
            self.author = info["Author"]
            self.name = info["Name"]

        else:
            raise no("Emtpy toons aren't allowed")
    def __getattr__(self, __name):
        s = ["url", "author", "name", "image", "key"]

        for x in s:
            if __name.lower() == x:
                return super(Toons, self).__getattribute__(__name.lower())
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Toon):
            return self.name == __o.name
    def __repr__(self):
        return f"<Toon name= '{self.name}' author= '{self.author}' url= '{self.url}'>"
class Daily:
    def __init__(self, genre):
        self.genre = genre
        self.toons = []

        self.url = "https://www.webtoons.com/en/dailySchedule"

        self.__get()
    def __repr__(self) -> str:

        return f"Results={str(self.toons)}"
    def __iter__(self):
        self.index = 0

        return self
    def __next__(self):
        max = len(self.toons)

        if self.index <= (max - 1):
            print(max)
            s = self.toons[self.index]

            self.index += 1
            return s
        else:
            raise StopIteration()
    def __getitem__(self, index):

        if isinstance(index, int):
            return self.toons[index]
        elif isinstance(index, slice):
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
                info = Toon(**self.__inform(x))
                self.toons.append(info)
        
    def __inform(self, t):
        name = t.find("p", class_="subj").text
        url = t["href"]
        author = t.find("p", class_="author").text
        img = t.find("img")["src"]

        img_cont = requests.get(img).text
        return {"Name" : name, "Author" : author, "Url" : url, "Img" : Image(name, img, format="png")}

