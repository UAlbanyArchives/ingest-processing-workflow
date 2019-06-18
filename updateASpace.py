import os
import csv
import openpyxl
import argparse

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
args = argParse.parse_args()

if os.name == 'nt':
    processingDir = "\\\\Romeo\\SPE\\processing"
else:
    processingDir = "/media/SPE/processing"

colID = args.package.split("_")[0].split("-")[0]
package = os.path.join(processingDir, colID, args.package)
derivatives = os.path.join(package, "derivatives")
metadata = os.path.join(package, "metadata")

if not os.path.isdir(package) or not os.path.isdir(derivatives) or not os.path.isdir(metadata):
    raise ("ERROR: " + package + " is not a valid package.")

hyraxImport = os.path.join(metadata, args.package + ".tsv")
if not os.path.isfile(hyraxImport):
    raise ("ERROR: " + hyraxImport + " is not a valid hryax import TSV.")
    
for sheetFile in os.listdir(metadata):
    if sheetFile.lower().endswith(".xlsx"):
        print ("Reading sheet: " + sheetFile)
        sheetPath = os.path.join(metadata, sheetFile)
        wb = openpyxl.load_workbook(filename=sheetPath, read_only=False)
        
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
                            refID = row[0].value
                            match = False
                            
                            file = open(hyraxImport, "r")
                            reader = csv.reader(file, delimiter='\t')
                            for line in reader:
                                if line[1].startswith("daos/"):
                                    if line[7] == refID:
                                        print ("Updating " + str(row[22].value) + " to " + str(line[1]))
                                        row[22].value = "https://archives.albany.edu/concern/" + line[1]
                                        match = True
                                        
                            file.close()
                            
                            if match == False:
                                print ("ERROR: failed to find matching refID " + refID + " in hyrax upload file " + hyraxImport)
        wb.save(filename=os.path.join(metadata, "updated_" + sheetFile))