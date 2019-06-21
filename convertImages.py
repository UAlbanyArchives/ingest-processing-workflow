import os
import shutil
import img2pdf
import argparse
from subprocess import Popen, PIPE

if os.name == 'nt':
    processingDir = "\\\\Romeo\\SPE\\processing"
    imagemagick = "magick"
    pdfCmd = ["pdftk", "cat output "]
else:
    processingDir = "/media/SPE/processing"
    imagemagick = "convert"
    pdfCmd = ["pdfunite", ""]
    
parser = argparse.ArgumentParser()
parser.add_argument("package", help="ID for package you are processing, i.e. 'ua950.012_Xf5xzeim7n4yE6tjKKHqLM'.")
parser.add_argument("-i", "--input", help="Input format for images, such as tiff, jpg, or png.")
parser.add_argument("-o", "--output", help="Output format, such as jpg, png, or pdf.")

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
dirList = [package, masters, derivatives, metadata]

def process(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if len(stdout) > 0:
        print (stdout)
    if len(stderr) > 0:
        print (stderr)

for path in dirList:
    if not os.path.isdir(path):
        raise Exception("ERROR: " + str(args.package) + " is not a valid processing package.")
if not args.input:
    raise Exception("ERROR: missing input format.")
if not args.output:
    raise Exception("ERROR: missing output format.")
if args.input.lower() == "tif" or args.input.lower()== "tiff":
    format1 = ".tif"
    format2 = ".tiff"
if args.input.lower() == "jpg" or args.input.lower()== "jpeg":
    format1 = ".jpg"
    format2 = ".jpeg"
else:
    format1 = "." + str(args.input)
    format2 = "." + str(args.input)

if args.output.lower() == "pdf":

    dirList = []
    for root, dirs, files in os.walk(masters):
        for file in files:
            if file.lower().endswith(format1) or file.lower().endswith(format2):
                if not root in dirList:
                    dirList.append(root)

    for folder in dirList:
        rootDir = []
        switch = False
        pathList = folder.split(os.path.sep)
        newFilename = pathList[-1]
        for item in pathList:
            if item == newFilename:
                switch = False
            if switch == True:
                rootDir.append(item)
            if item == "masters":
                switch = True
        if len(rootDir) > 0:
            relPath = os.path.join(derivatives, os.path.sep.join(rootDir))
            if not os.path.isdir(relPath):
                os.makedirs(relPath)
        else:
            relPath = derivatives
        
        pageList = []
        outputPath = os.path.join(relPath, newFilename + ".pdf")
        if args.input.lower() == "pdf":
            for inputFile in os.listdir(folder):
                if inputFile.lower().endswith(format1):
                    pageList.append("\'" + os.path.join(folder, inputFile) + "\'")
            cmd = [pdfCmd[0], " ".join(pageList), pdfCmd[1] + "\'" + outputPath + "\'"]
            #print (" ".join(cmd))
            #print ("\n\n")
            process(" ".join(cmd))
        else:
            convertDir = os.path.join(package, "converting")
            if not os.path.isdir(convertDir):
                os.mkdir(convertDir)
            for inputFile in os.listdir(folder):
                if inputFile.lower().endswith(format1) or inputFile.lower().endswith(format2):
                    convertFile = os.path.join(convertDir, os.path.splitext(inputFile)[0] + ".jpg")
                    print ("compressing " + inputFile + "...")
                    cmd = [imagemagick, os.path.join(folder, inputFile), convertFile]
                    process(cmd)
                    pageList.append(convertFile)
            if os.path.isfile(outputPath):
                print ("skipping, as " + newFilename + ".pdf already exists.")
            else:
                print ("converting " + newFilename + " to " + outputPath)
                #print(pageList)
                f = open(outputPath, "wb")
                f.write(img2pdf.convert(pageList))
                f.close()
            shutil.rmtree(convertDir)
            
        
else:
    for root, dirs, files in os.walk(masters):
        for file in files:
            if file.lower().endswith(format1) or file.lower().endswith(format2):
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
                
                outputFile = os.path.join(relPath, os.path.splitext(file)[0] + "." + str(args.output))
                if os.path.isfile(outputFile):
                    print ("skipping, as " + str(os.path.splitext(file)[0] + "." + str(args.output)) + " already exists.")
                else:
                    print ("converting " + file + " to " + str(args.output))
                    cmd = [imagemagick, fullPath, outputFile]
                    process(cmd)
        
        
        
        