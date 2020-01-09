import os
import csv
from subprocess import Popen, PIPE

from tokenize import tokenize
from bs4 import BeautifulSoup

sheetFile = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/metadata/ua435_nDmescjNLkkjigbozTXSTY.tsv"
hyraxSheetFile = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/metadata/out-ua435_nDmescjNLkkjigbozTXSTY.tsv"
abstractFiles = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/derivatives/proceedings"

hyraxSheet = []

abstractData = {}
for abstractYear in os.listdir(abstractFiles):
    lookDir = os.path.join(abstractFiles, abstractYear)
    print (lookDir)
    for root, dirs, files in os.walk(lookDir):
        for file in files:
            #print (file)
            if "withabstract" in file.lower():
                if file.lower().endswith("html") or file.lower().endswith("htm"):
                    abstractPath = os.path.join(root, file)
                    print (abstractPath)
                    f = open(abstractPath, "r", encoding='windows-1252', newline='')
                    soup = BeautifulSoup(f, 'html.parser')
                    abstractData[abstractYear] = soup
                    f.close()
                    
infile = open(sheetFile, "r", encoding='utf-8', newline='')
reader = csv.reader(infile, delimiter='\t', lineterminator='\n')

def clearSpan(para):
    #print (para)
    if para.span:
        cleanPara = para.span.replace_with(" ")
        para = clearSpan(para)
        return para
    else:
        #print ("test3")
        return para

count = 0
for row in reader:
    count += 1
    if count > 1:
        found = False
        title = row[9]
        filename = os.path.basename(row[2]).strip()
        year = row[11]
        #print (filename)
        #print (title)
        soup = abstractData[year]
        #print (soup.title)
        match = None
        for link in soup.find_all('a', href=True):
            if not link['href'] is None:
                #print (filename + " --> " + link['href'])
                #print (filename in link['href'])
                if filename in link['href']:
                    
                    #print (link)
                    if found == True:
                        pass
                        #print ("!!! " + year)
                        #print (filename)
                        #print (link.string)
                    else:
                        found = True
                        yearList = ["1994", "1995", "1996"]
                        #print (year)
                        if year in yearList:
                            
                            nextText = link.parent.find_next('p').text
                            if link.parent.find_next('p').b:
                                skipB = link.parent.find_next('p').find_next('p').text
                                if len(skipB.strip()) < 1:
                                    para = link.parent.find_next('p').find_next('p').find_next('p')
                                    cleanPara = clearSpan(para)
                                    nextText = cleanPara.text
                                else:
                                    para = link.parent.find_next('p').find_next('p')
                                    cleanPara = clearSpan(para)
                                    nextText = cleanPara.text
                            else:
                                if len(nextText.strip()) < 1:
                                    para = link.parent.find_next('p').find_next('p')
                                    cleanPara = clearSpan(para)
                                    nextText = cleanPara.text
                                else:
                                    para = link.parent.find_next('p')
                                    cleanPara = clearSpan(para)
                                    nextText = cleanPara.text
                                    
                            
                        else:
                            nextText = link.find_next('p').text
                        
                            
                        if "abstract" in nextText.lower():
                            match = nextText.replace("Abstract: ", "").replace("Abstract", "").replace("\r", "").replace("\n", "").strip()
                            #print (count)
                            #print (filename)
                            #print (year)
                            #print (title)
                            #print ("\t" + match)
                            
                        elif year == "1994" and len(nextText.strip()) > 25:
                            
                            match = nextText.replace("Abstract: ", "").replace("Abstract", "").replace("\r", " ").replace("\n", " ").strip()
                            #if link['href'] == "papers_vol_2/masha130.pdf":
                            #    print ("test")
                            #    print (match)
                            #print (count)
                            #print (filename)
                            #print (year)
                            #print (title)
                            #print ("\t" + match)
                        else:   
                            pass
                            #print (count)
                            #print (filename)
                            #print (year)
                            #print (title)
        
        if found == False:
            pass
            #print (count)
            #print (filename)
            #print ("cannot find year " + year + ": " + title)
        else:
            #next = link.parent.find_next_sibling('p')
            #print (match)
            row[10] = match
            
    hyraxSheet.append(row)
            
if os.path.isfile(hyraxSheetFile):
    outfile = open(hyraxSheetFile, "a", newline='')
    writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
else:
    outfile = open(hyraxSheetFile, "w", newline='')
    writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
for object in hyraxSheet:
    #print (object[9])
    writer.writerow(object)
outfile.close()
            
infile.close()
"""

def process(cmd):
    print (" ".join(cmd))

    p = Popen(" ".join(cmd), shell=True, stdout=PIPE, stderr=PIPE)
    #p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if len(stdout) > 0:
        print (stdout)
    if len(stderr) > 0:
        print (stderr)


dir = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/derivatives/proceedings/1997"


for filename in os.listdir(dir):
    cmd = ["wkhtmltopdf", "--margin-top 20mm", "--margin-bottom 20mm", "--margin-left 20mm", "--margin-right 20mm"]
    if filename.lower().endswith("htm"):
        file = os.path.join(dir, filename)
        outfile = os.path.join(dir, os.path.splitext(filename)[0] + ".pdf")
        cmd.append(file)
        cmd.append(outfile)
        process(cmd)
"""