from webtoon import Daily, sendit 
from time import sleep

toons = Daily("drama")

print(toons[0].author)