import os
import argparse

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
args = argParse.parse_args()

if os.name == 'nt':
    processingDir = "\\\\Romeo\\SPE\\processing"
    sipDir = "\\\\Lincoln\\Masters\\Archive\\SIP"
else:
    sipDir = "/media/Masters/Archive/SIP"

colID = args.package.split("_")[0].split("-")[0]
package = os.path.join(processingDir, colID, args.package)
masters = os.path.join(package, "masters")

if not os.path.isdir(package) or not os.path.isdir(masters):
    raise ("ERROR: " + package + " is not a valid package.")
    
print ("does not work yet")