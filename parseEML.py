import os
import email
import argparse
from subprocess import Popen, PIPE

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

senders = []
recievers = []

for root, dirs, files in os.walk(derivatives):
    for file in files:
        if file.lower().endswith("eml"):
            filePath = os.path.join(root, file)
            
            file = open(filePath, "r")
            raw_email = file.read()
            msg = email.message_from_string(raw_email)
            if msg["from"] not in senders:
                senders.append(msg["from"])
            if msg["from"] not in recievers:
                recievers.append(msg["from"])
            file.close()