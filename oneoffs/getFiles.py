import os
import shutil

folder = "/media/SPE/processing/ua802.011/ua802.011_xEGv4TDCdynUbQENG9TSbd/derivatives/SUNY-ALBANY_15326_Scrapbooks"
jpgs = "/media/SPE/processing/ua802.011/ua802.011_xEGv4TDCdynUbQENG9TSbd/derivatives/jpgs"

print ("start")
for root, dirs, files in os.walk(folder):
    for file in files:
        path = os.path.join(root, file)
        print (file)
        shutil.move(path, jpgs)
        