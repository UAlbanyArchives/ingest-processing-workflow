import os
import argparse
from tqdm import tqdm
from subprocess import Popen, PIPE

if os.name == 'nt':
    processingDir = "\\\\Lincoln\\Library\\SPE_Processing\\backlog"
else:
    processingDir = "/media/Library/SPE_Processing/backlog"

parser = argparse.ArgumentParser()
parser.add_argument("package", help="ID for package you are processing, i.e. 'ua950.012_Xf5xzeim7n4yE6tjKKHqLM'.")
parser.add_argument("-p", "--path", help="Subpath, relative to derivatives directory which will only convert files there.", default=None)

args = parser.parse_args()

if "_" in args.package:
    ID = args.package.split("_")[0]
elif "-" in args.package:
    ID = args.package.split("-")[0]
else:
    raise Exception("ERROR: " + str(args.package) + " is not a valid processing package.")
    
package = os.path.join(processingDir, ID, args.package)
masters = os.path.join(package, "masters")
derivatives = os.path.join(package, "derivatives")
metadata = os.path.join(package, "metadata")

def process(cmd):
    #p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if len(stdout) > 0:
        print (stdout)
    if len(stderr) > 0:
        print (stderr)



if args.path:
    ocrPath = os.path.join(derivatives, os.path.normpath(args.path))
    if not os.path.isdir(derivatives):
        raise Exception("ERROR: subpath " + args.path + " relative to derivatives is not a valid path.")
else:
    ocrPath = derivatives

for root, dirs, files in os.walk(ocrPath):
    for file in tqdm(files):
        if file.lower().endswith(".pdf"):
            #cmd = ["ocrmypdf", "--deskew", "--clean"]
            cmd = ["ocrmypdf", "--deskew"]
            filepath = os.path.join(root, file)
            cmd.append(filepath)
            cmd.append(filepath)

            #print ("\n\n")
            #print (" ".join(cmd))
            print ("processing " + file + "...")
            process(cmd)
