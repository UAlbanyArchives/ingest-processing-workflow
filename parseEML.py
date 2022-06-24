import os
from email import policy
from email.parser import BytesParser
from email.iterators import _structure
import argparse
from subprocess import Popen, PIPE

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
args = argParse.parse_args()

if os.name == 'nt':
    processingDir = "\\\\Lincoln\\Library\\SPE_Processing\\backlog"
else:
    processingDir = "/media/Library/SPE_Processing/backlog"

colID = args.package.split("_")[0].split("-")[0]
package = os.path.join(processingDir, colID, args.package)
derivatives = os.path.join(package, "derivatives")

if not os.path.isdir(package) or not os.path.isdir(derivatives):
    raise ("ERROR: " + package + " is not a valid package.")

senders = []
recievers = []

outfile = os.path.join(derivatives, "test.html")

count = 0
for root, dirs, files in os.walk(derivatives):
    for file in files:
        if file.lower().endswith("eml"):
            count += 1
            filePath = os.path.join(root, file)
            
            if count == 30:
                with open(filePath, 'rb') as fp:
                    msg = BytesParser(policy=policy.default).parse(fp)
                #text = msg.get_body(preferencelist=('plain')).get_content()
                #print(text)
                for part in msg.walk():
                    print(part.get_content_type())
                    if part.get_content_type() == "text/html":
                        #print (part)
                        file = open(outfile, "w")
                        file.write(str(part))
                        file.close()
                print ("thats the type list")
                #_structure(msg)
                print (msg['To'])
                print (msg['From'])
                print (msg['Subject'])
                """
                file = open(filePath, "rb")
                raw_email = file.read()
                msg = email.message_from_string(raw_email)
                if msg["from"] not in senders:
                    senders.append(msg["from"])
                if msg["from"] not in recievers:
                    recievers.append(msg["from"])
                file.close()
                """
