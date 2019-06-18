import os
import csv
import requests
import argparse
import openpyxl

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
args = argParse.parse_args()

if os.name == 'nt':
    processingDir = "\\\\Romeo\\SPE\\processing"
    #ESPYderivatives = "\\\\Lincoln\Library\ESPYderivatives"
else:
    processingDir = "/media/SPE/processing"
    #ESPYderivatives = "/media/Library/ESPYderivatives"

colID = args.package.split("_")[0].split("-")[0]
package = os.path.join(processingDir, colID, args.package)
derivatives = os.path.join(package, "derivatives")
metadata = os.path.join(package, "metadata")

hyraxHeaders = ["Type", "URIs", "File Paths", "Accession", "Collecting Area", "Collection Number", "Collection", "ArchivesSpace ID", \
"Record Parents", "Title", "Description", "Date Created", "Resource Type", "License", "Rights Statement", "Subjects", "Whole/Part",\
"Processing Activity", "Extent", "Language"]

hyraxSheetFile = os.path.join(metadata, args.package + ".tsv")
#hyraxImport = os.path.join(ESPYderivatives, "import")
#hyraxFiles = os.path.join(ESPYderivatives, "files", colID)
#if not os.path.isdir(hyraxFiles):
#    os.mkdir(hyraxFiles)

if not os.path.isdir(package) or not os.path.isdir(derivatives) or not os.path.isdir(metadata):
    raise ("ERROR: " + package + " is not a valid package.")
    
collectionData = requests.get("https://archives.albany.edu/collections/catalog/" + colID.replace(".", "-") + "?format=json", verify=False).json()
collectingArea = collectionData["response"]["document"]["repository_ssm"][0]
collection = collectionData["response"]["document"]["title_ssm"][0]
processingNote = "Processing documentation available at: https://wiki.albany.edu/display/SCA/Processing+Ingested+Digital+Files"

# make hyrax sheet
hyraxSheet = []
    
for sheetFile in os.listdir(metadata):
    if sheetFile.lower().endswith(".xlsx"):
        print ("Reading sheet: " + sheetFile)
        sheetPath = os.path.join(metadata, sheetFile)
        wb = openpyxl.load_workbook(filename=sheetPath, read_only=True)
        
        #validate sheets
        for sheet in wb.worksheets:
            checkSwitch = True
            try:
                if sheet["H1"].value.lower().strip() != "title":
                    checkSwitch = False
                elif sheet["H2"].value.lower().strip() != "level":
                    checkSwitch = False
                elif sheet["H3"].value.lower().strip() != "ref id":
                    checkSwitch = False
                elif sheet["J6"].value.lower().strip() != "date 1 display":
                    checkSwitch = False
                elif sheet["D6"].value.lower().strip() != "container uri":
                    checkSwitch = False
            except:
                print ("ERROR: incorrect sheet " + sheet.title + " in file " + sheetPath)
                
            if checkSwitch == False:
                print ("ERROR: incorrect sheet " + sheet.title + " in file " + sheetPath)
            else:              
                
                rowCount = 0
                for row in sheet.rows:
                    rowCount = rowCount + 1
                    if rowCount > 6:
                        if not row[22].value is None:
                            if not row[0].value and row[8].value and row[9].value:
                                raise ("ERROR: Row " + str(rowCount) + " is invalid (" + str(row[22].value) + ").")
                            else:
                                refID = row[0].value
                                title = row[8].value
                                date = row[9].value
                                print ("\tReading " + str(title) + "...")
                                itemData = requests.get("https://archives.albany.edu/collections/catalog/" + colID.replace(".", "-") + "aspace_" + refID + "?format=json", verify=False).json()
                                parentList = []
                                for parent in itemData["response"]["document"]["parent_ssm"][1:]:
                                    parentList.append(parent.split("_")[1])
                                parents = "|".join(parentList)
                                hyraxObject = ["DAO", "", row[22].value, args.package, collectingArea, colID, collection, refID, parents, title, "", date, \
                                "", "", "", "", "whole", processingNote, "", ""]
                                
                                hyraxSheet.append(hyraxObject)
                                

outfile = open(hyraxSheetFile, "w")
writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
writer.writerow(hyraxHeaders)
for object in hyraxSheet:
    writer.writerow(object)
outfile.close()