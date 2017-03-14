import os
import sys
from HTMLParser import HTMLParser

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        
        for attr in attrs:
            print("     attr:", attr)
            wf.write('\n '.join(str(s) for s in attr));
            
    def handle_data(self, data):
        #print("Data     :", data)
        wf.write(data.strip());
        
f = open(os.path.join(sys.path[0],"data\\test.html"),'r')
wf = open(os.path.join(sys.path[0],"data\\testScrub.txt"),'w')


print("test");


parser = HTMLParser()
parser.feed(f.readline())

'''
for line in f.read().split("<div"):
    wf.write(line +"\n")
'''


f.close()
wf.close()


