import os
import shutil
import argparse
from packages.SIP import SubmissionInformationPackage

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
args = argParse.parse_args()

if os.name == 'nt':
    processingDir = "\\\\Lincoln\\Library\\SPE_Processing\\backlog"
    sipDir = "\\\\Lincoln\\Masters\\Archives\\SIP"
else:
    processingDir = "/media/Library/SPE_Processing/backlog"
    sipDir = "/media/Masters/Archives/SIP"

colID = args.package.split("_")[0].split("-")[0]
package = os.path.join(processingDir, colID, args.package)
masters = os.path.join(package, "masters")
sipPackage = os.path.join(sipDir, colID, args.package)
sipMasters = os.path.join(sipPackage, "data")

if not os.path.isdir(package) or not os.path.isdir(masters) or not os.path.isdir(sipPackage):
    raise ("ERROR: " + str(package) + " is not a valid package.")
    
sipPackage = os.path.join(sipDir, colID, args.package)
print ("Loading SIP...")
SIP = SubmissionInformationPackage()
SIP.load(sipPackage)
print ("Validating SIP...")
if SIP.bag.is_valid():
    for thing in os.listdir(masters):
        print ("Removing " + thing + "...")
        path = os.path.join(masters, thing)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    for thing in os.listdir(sipMasters):
        print ("Moving " + thing + "...")
        path = os.path.join(sipMasters, thing)
        if os.path.isdir(path):
            shutil.copytree(path, os.path.join(masters, thing))
        else:
            shutil.copy2(path, masters)
else:
    raise ("ERROR: " + str(package) + " is not a valid bag!")
