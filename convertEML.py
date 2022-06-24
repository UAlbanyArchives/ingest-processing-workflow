import os
import argparse
from subprocess import Popen, PIPE

argParse = argparse.ArgumentParser()
argParse.add_argument("package", help="Package ID in Processing directory.")
args = argParse.parse_args()

if os.name == 'nt':
    processingDir = "\\\\Lincoln\\Library\\SPE_Processing\\backlog"
else:
    processingDir = "/media/Library/SPE_Processing/backlog"

def process(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if len(stdout) > 0:
        print (stdout)
    if len(stderr) > 0:
        print (stderr)

colID = args.package.split("_")[0].split("-")[0]
package = os.path.join(processingDir, colID, args.package)
derivatives = os.path.join(package, "derivatives")

if not os.path.isdir(package) or not os.path.isdir(derivatives):
    raise ("ERROR: " + package + " is not a valid package.")
    
# Requires https://github.com/nickrussler/eml-to-pdf-converter in Home directory and wkhtmltopdf in PATH
jar = os.path.expanduser("~/emailconverter-2.0.1-all.jar")
if not os.path.isfile(jar):
     raise ("ERROR: Requires https://github.com/nickrussler/eml-to-pdf-converter in Home directory and wkhtmltopdf in PATH.")
    

for root, dirs, files in os.walk(derivatives):
    for file in files:
        if file.lower().endswith("eml"):
            fullPath = os.path.join(root, file)
            switch = False
            folders = []
            for item in root.split(os.path.sep):
                if switch == True:
                    folders.append(item)
                if item == "masters":
                    switch = True
            
            relPath = os.path.join(derivatives, os.path.sep.join(folders))
            if not os.path.isdir(relPath):
                os.makedirs(relPath)
            
            outputFile = os.path.join(relPath, os.path.splitext(file)[0] + ".pdf")
            if os.path.isfile(outputFile):
                print ("skipping, as " + str(os.path.splitext(file)[0] + ".pdf already exists."))
            else:
                print ("converting " + file + " to PDF.")
                cmd = ["java", "-jar", jar, fullPath, "-o", outputFile]
                process(cmd)
