import os
import argparse
from packages.SIP import SubmissionInformationPackage

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
args = argParse.parse_args()

if os.name == 'nt':
    raise ("ERROR: Must be run from processing server.")
else:
    sipDir = "/media/Masters/Archives/SIP"

colID = args.package.split("_")[0].split("-")[0]
sipPackage = os.path.join(sipDir, colID, args.package)

SIP = SubmissionInformationPackage()
SIP.load(sipPackage)
SIP.safeRemove()
sipParent = os.path.join(sipDir, colID)
if len(os.listdir(sipParent)) == 0:
    os.rmdir(sipParent)