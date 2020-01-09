import os
from tika import parser

path = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/masters/proceedings/1999/PAPERS"
path = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/masters/proceedings/1999/HOME.PDF"

raw = parser.from_file(path)
list = raw['content'].split("System Dynamics Approach, Wiley.")[1]

count = 0
for line in list.split("\n"):
    count += 1
    if count < 100:
        print (line)

"""
for pdfFile in os.listdir(path):

    if pdfFile.lower().endswith("para65.pdf"):
        
        raw = parser.from_file(os.path.join(path, pdfFile))
        head, body = raw['content'].split("Abstract")
        
        title = None
        title2 = None
        author = None
        switch = False
        count = 0
        #print (head)
        for line in head.split("\n"):
            count += 1
            #print (str(count) + ": " + line)
            if len(line.strip()) > 0:
                if title is None:
                    title = line
                elif title2 is None:
                    if switch is False:
                        title2 = line
                elif author is None:
                    if switch is False:
                        author = line
                switch = True
            else:
                switch = False
        
        abstract = ""
        empty = False
        print (body)
        for line in body.split("\n"):
            if empty == False:
                if len(line.strip()) > 0:
                    abstract = abstract + " " + line
                else:
                    if len(abstract) > 0:
                        empty = True
            
                
        print (author)
        print ("\t" + title)
        print (abstract)
"""