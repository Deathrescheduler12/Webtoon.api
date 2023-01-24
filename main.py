from webtoon import Daily
from notifw import send

toons = Daily("drama")

print(send(toons[0]))
