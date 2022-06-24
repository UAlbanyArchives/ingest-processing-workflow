import os
import csv
import requests
import argparse
import openpyxl

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
argParse.add_argument("-f", "--file", help="File name of spreadsheet to be updated. If no files are listed, all will be updated.", default=None)
args = argParse.parse_args()

if os.name == 'nt':
    processingDir = "\\\\Lincoln\\Library\\SPE_Processing\\backlog"
    #ESPYderivatives = "\\\\Lincoln\Library\ESPYderivatives"
else:
    processingDir = "/media/Library/SPE_Processing/backlog"
    #ESPYderivatives = "/media/Library/ESPYderivatives"

colID = args.package.split("_")[0].split("-")[0]
package = os.path.join(processingDir, colID, args.package)
derivatives = os.path.join(package, "derivatives")
masters = os.path.join(package, "masters")
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
    
collectionData = requests.get("https://archives.albany.edu/description/catalog/" + colID.replace(".", "-") + "?format=json", verify=False).json()
collectingArea = collectionData["data"]["attributes"]["repository_ssm"]["attributes"]["value"][0]
collection = collectionData["data"]["attributes"]["title_ssm"]["attributes"]["value"][0]
processingNote = "Processing documentation available at: https://wiki.albany.edu/display/SCA/Processing+Ingested+Digital+Files"

# make hyrax sheet
hyraxSheet = []

#function to read ASpace tree to get parent ref_ids
def getParents(obj, parentList, level, objURI):
    level += 1
    for child in obj["children"]:
        if level == 1:
            parentList = []
        if child["record_uri"] == objURI:
            return parentList
        else:
            parentRefID = client.get(child["record_uri"]).json()["ref_id"]
            parentList.append(parentRefID)
            getParents(child, parentList, level, objURI)

warningList = [] 
for sheetFile in os.listdir(metadata):
    if sheetFile.lower().endswith(".xlsx") and not sheetFile.lower().startswith("~$"):
        if not args.file or args.file.lower() == sheetFile.lower():
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
                    tree = None
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
                                    arclight = requests.get("https://archives.albany.edu/description/catalog/" + colID.replace(".", "-") + "aspace_" + refID + "?format=json", verify=False)
                                    if arclight.status_code == 200:
                                        parentList = []
                                        itemData = arclight.json()
                                        for parent in itemData["data"]["attributes"]["parent_ssim"]["attributes"]["value"][1:]:
                                            parentList.append(parent.split("_")[1])
                                        parents = "|".join(parentList)
                                    else:
                                        #for new objects not yet indexed in ArcLight
                                        if tree is None:                                        
                                            from asnake.client import ASnakeClient
                                            client = ASnakeClient()
                                            client.authorize()
                                            
                                            ref = client.get("repositories/2/find_by_id/archival_objects?ref_id[]=" + refID).json()
                                            item = client.get(ref["archival_objects"][0]["ref"]).json()
                                            resource = client.get(item["resource"]["ref"]).json()
                                            tree = client.get(resource["tree"]["ref"]).json()
                                        else:
                                            ref = client.get("repositories/2/find_by_id/archival_objects?ref_id[]=" + refID).json()
                                            
                                        objURI = ref["archival_objects"][0]["ref"]
                                        parentList = []
                                        parentList = getParents(tree, parentList, 0, objURI)
                                        print (parentList)
                                        parents = "|".join(parentList)                                            
                                    
                                    derivativesDao = os.path.join(derivatives, row[22].value)
                                    masterDao = os.path.join(masters, row[22].value)
                                    if not os.path.isfile(derivativesDao) and not os.path.isfile(masterDao):
                                        print ("WARNING: DAO filename \"" + row[22].value + "\" does not exist in package.")
                                        warningList.append(row[22].value)
                                    
                                    hyraxObject = ["DAO", "", row[22].value, args.package, collectingArea, colID, collection, refID, parents, title, "", date, \
                                    "", "", "", "", "whole", processingNote, "", ""]
                                    
                                    hyraxSheet.append(hyraxObject)
                                
if os.path.isfile(hyraxSheetFile):
    outfile = open(hyraxSheetFile, "a", encoding='utf-8', newline='')
    writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
else:
    outfile = open(hyraxSheetFile, "w", encoding='utf-8', newline='')
    writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
    writer.writerow(hyraxHeaders)
for object in hyraxSheet:
    #print (object[9])
    writer.writerow(object)
outfile.close()

if len(warningList) > 0:
    print ("WARNING: the following files were not found in package:")
    print ("\t" + "\n\t".join(warningList))
