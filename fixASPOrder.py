import os
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
masters = os.path.join(package, "masters")

if not os.path.isdir(package) or not os.path.isdir(masters):
    raise ("ERROR: " + package + " is not a valid package.")
    
dirList = []
for root, dirs, files in os.walk(masters):
    for file in files:
        if file.lower().endswith("pdf"):
            if not root in dirList:
                dirList.append(root)
                
for folder in dirList:
    for file in os.listdir(folder):
        originalPath = os.path.join(folder, file)
        filename, ext = os.path.splitext(file)
        charList = []
        endswitch = False
        for char in reversed(filename):
            if endswitch == False:
                try:
                    int(char)
                    charList.append(char)
                except:
                    endswitch = True
        if len(charList) == 1:
            newFilename = filename[:-1] + "0" + charList[0]
            print ("Changing " + filename + " to " + newFilename)
            os.rename(originalPath, os.path.join(folder, newFilename + ext))