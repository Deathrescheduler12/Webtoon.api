from win10toast_click import ToastNotifier
import webbrowser as webb
from webtoon import Webtoon
import os

toast = ToastNotifier()

def send(toon: Webtoon):
    path = os.path.join(toon.image.path, "webtoon.png")
    toast.show_toast(
        toon.name,
        "Daily Action toons!",
        path,
        10,
        True,
        lambda: webb.open(toon.url)
    )