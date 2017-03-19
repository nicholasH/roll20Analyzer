import re
from bs4 import BeautifulSoup



def getParse(path):
    f = open(path)
    soup = BeautifulSoup(f.read(), 'html.parser')  # make soup that is parse-able by bs

    generalmatch = re.compile('message \w+')

    chatContent = soup.findAll("div", {"class": generalmatch})

    f.close()
    return chatContent

