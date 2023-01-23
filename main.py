from webtoon import Daily
from notifw import send

from time import sleep

toons = Daily("drama")

print(send(toons[0]))
