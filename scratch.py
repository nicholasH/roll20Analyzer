from bs4 import BeautifulSoup
import re
from bs4.element import NavigableString
from datetime import datetime, timedelta


def getParse(path):
    f = open(path)
    soup = BeautifulSoup(f.read(), 'html.parser')  # make soup that is parse-able by bs
    f.close()
    generalmatch = re.compile('message \w+')

    chatContent = soup.findAll("div", {"class": generalmatch})
    # print(chatContent)

    return chatContent


def rollbackHours(path,hoursBack):
    chatContent = getParse(path)
    hoursBack = hoursBack * 3600
    first = True
    firstTime = ""

    for index, chat in enumerate(reversed(chatContent)):
        for ch in chat.contents:
            if not isinstance(ch, NavigableString):
                s = ch.attrs.get("class")
                if not isinstance(s, type(None)):
                    if any("tstamp" in f for f in s):
                        timeSplit = ch.string.split()
                        time = timeSplit.pop()
                        chTime = datetime.strptime(time, '%I:%M%p')

                        if first:
                            firstTime = chTime
                            first = False
                        elif chTime < firstTime - timedelta(seconds = hoursBack):
                            return
    return chatContent






