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
derivatives = os.path.join(package, "derivatives")

if not os.path.isdir(package) or not os.path.isdir(derivatives):
    raise ("ERROR: " + package + " is not a valid package.")
    
# open the output file
f = open(os.path.join(package, 'derivatives.txt'), 'w')

#get all files in dao folder
for root, dirs, files in os.walk(derivatives):
    for file in files:
        filePath = os.path.join(root, file).split(derivatives)[1]
        if filePath.startswith("\\"):
            filePath = filePath[1:]
        if filePath.startswith("/"):
            filePath = filePath[1:]
        print ("writing " + filePath)
        f.write(filePath + "\n")
        
# close the output file
f.close()