import os
import csv
from bs4 import BeautifulSoup


input = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/derivatives/proceedings/2005/pictures/index.html"

f = open(input, "r", encoding='windows-1252', newline='')
soup = BeautifulSoup(f, 'html.parser')
pathRoot = "proceedings/2005/pictures/"
root = "/media/SPE/processing/ua435/ua435_nDmescjNLkkjigbozTXSTY/derivatives/"
sheet = []

for section in soup.findAll('center'):
    if section.find('h4'):
        title = section.find('h4').text
        print (title)
        files = []
        for a in section.findAll('a'):
            file = a["href"]
            if file.startswith("./"):
               file = file[2:]
            file = pathRoot + file
            files.append(file)
        sheet.append([title, "|".join(files)])

with open('/media/SPE/out.tsv', 'w', encoding='windows-1252', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for line in sheet:
        writer.writerow(line)
    
    """
    filename, ext = os.path.splitext(img["src"])
    if filename.endswith("_t"):
        file = filename[:-2] + ext
    else:
        file = filename + ext
    
    
    container = img.find_parent('a').find_parent('font')
    file = img.find_parent('a')["href"].replace("%20", " ")
    if len(file) > 0:
        #print (file)
        desc = ""
        if container.text:
            desc = desc + " " + container.text
        for font in container.findAll('font'):
            #count = 0
            #for text in font.stripped_strings:
            #    count += 1
            #    if count == 1:
            #        desc = text
            desc = desc + " " + font.text
            for text in font.findAll():
                desc = desc + " " + text.text
        desc = desc.strip().replace("         ", " ").replace("\n", " ").replace("\r", "").replace("         ", " ").replace("  ", " ")
        if desc.split(" ")[-1] == "KB":
            desc = " ".join(desc.split(" ")[:-2])
        
        print ("\t" + desc)
        if desc in sheet.keys():
            if not os.path.isfile(root + pathRoot + file):
                raise ValueError(pathRoot + file)
            obj = sheet[desc] + "|" + pathRoot + file
            sheet[desc] = obj
        else:
            obj = pathRoot + file
            sheet[desc] = obj
    """
#for thing in sheet.keys():
#    print (thing + ";" + sheet[thing])

f.close()