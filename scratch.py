from html.parser import HTMLParser

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        
        for attr in attrs:
            print("     attr:", attr)
            wf.write(' '.join(str(s) for s in attr) + '\n');
            
    def handle_data(self, data):
        f
        #print("Data     :", data)
        wf.write(data.strip() +"\n");
        

f = open("E:\\GitProjects\\roll20Analyzer\\data\\test.html",'r')
wf = open("E:\\GitProjects\\roll20Analyzer\\data\\scrub.txt",'w')




parser = HTMLParser()

parser.feed(f.readline())



f.close()
wf.close()


