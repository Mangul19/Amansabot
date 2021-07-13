from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import time

while(True):
    listin = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

    rand = random.randint(0, 99)

    if rand >= 10:
        rand = "000" + str(rand)
    else:
        rand = "0000" + str(rand) 

    html = urlopen("http://mangul.iptime.org/" + random.choice(listin) + "." + rand)  
    bsObject = BeautifulSoup(html, "html.parser").select("body")

    print(bsObject)

    time.sleep(0.5)