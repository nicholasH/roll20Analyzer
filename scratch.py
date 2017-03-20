from bs4 import BeautifulSoup
import re
from bs4.element import NavigableString
from datetime import datetime





test = []
f = open("E:\\GitProjects\\roll20Analyzer\\data\\Chat Log for Caramohn's Level.html")


soup = BeautifulSoup(f.read(), 'html.parser')  # make soup that is parse-able by bs
f.close()

generalmatch = re.compile('message \w+')

chatContent = soup.findAll("div", {"class": generalmatch})




def getTimeRange():
    date1String = "Aug 26 2016"
    date1 = datetime.strptime(date1String, '%b %d %Y')
    date2String = "OCT 29 2016"
    date2 = datetime.strptime(date2String,'%b %d %Y' )

    startMessageIndex = 0
    startFound = False
    endMessageIndex = len(chatContent)

    for index, chat in enumerate(chatContent):
        for ch in chat.contents:
            if not isinstance(ch, NavigableString):
                s = ch.attrs.get("class")
                if not isinstance(s, type(None)):
                    if any("tstamp" in f for f in s):
                        chDate = datetime.strptime(ch.string,'%B %d, %Y %I:%M%p')
                        if chDate.date() >= date1.date() and not startFound:
                            startMessageIndex = index
                            startFound = True
                        if date2.date() < chDate.date():
                            endMessageIndex = index -1
                            return [startMessageIndex,endMessageIndex]

    return [startMessageIndex,endMessageIndex]


tr =getTimeRange()


c = chatContent[tr[0]:tr[1]]





print()

