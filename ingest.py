import os
import sys
import json
import bagit
from listFiles import listFiles
from packages.SIP import SubmissionInformationPackage

#version of ingest.py
version = "0.1"
defaultPath = "/media/SPE/ingest"


def main(ID, path=None, accession=None):

    if path == None:
        if not os.path.isdir(defaultPath):
            raise Exception("ERROR: default path " + defaultPath  + " does not exist.")
        path = os.path.join(defaultPath, ID)
        if not os.path.isdir(path):
            raise Exception("ERROR: no " + ID + " directory exists for ingest in " + defaultPath)
    else:
        if not os.path.isdir(path):
            raise Exception("ERROR: " + str(path) + " is not a valid path.")        
    print ("Reading " + path)
        
            
    if accession == None:
        print ("Building SIP...")
        SIP = SubmissionInformationPackage()
        SIP.create(ID)
        SIP.package(path)
        print ("SIP " + SIP.bagID + " created.")

    else:
        print ("Reading accession " + accession)
        import asnake.logging as logging
        from asnake.client import ASnakeClient
        client = ASnakeClient()
        client.authorize()

        logging.setup_logging(stream=sys.stdout, level='INFO')
        
        call = "repositories/2/search?page=1&aq={\"query\":{\"field\":\"identifier\", \"value\":\"" + accession + "\", \"jsonmodel_type\":\"field_query\"}}"
        accessionResponse = client.get(call).json()
        if len(accessionResponse["results"]) < 1:
            raise Exception("ERROR: Could not find accession with ID: " + accession)
        else:
            accessionObject = json.loads(accessionResponse["results"][0]["json"])
            if "id_1" in accessionObject.keys():
                accessionID = accessionObject["id_0"] + "-" + accessionObject["id_1"]
            if accession != accessionID:
                raise Exception("ERROR: Could not find exact accession with ID: " + accession)
            if not "content_description" in accessionObject.keys():
                raise Exception("ERROR: no content description in " + accessionID + " accession, " + accessionObject["uri"])
            if len(accessionObject["related_resources"]) < 1:
                raise Exception("ERROR: no related resource for " + accessionID + " accession, " + accessionObject["uri"])
            else:
                resource = client.get(accessionObject["related_resources"][0]["ref"]).json()
                creator = resource["title"]
                if not ID.lower() == resource["id_0"].lower():
                    raise Exception("ERROR: accession " + accessionID + " does not link to collection ID " + ID + ". Instead linked to " + resource["id_0"])
                description = accessionObject["content_description"]
                
                print ("Building SIP...")
                SIP = SubmissionInformationPackage()
                SIP.create(ID)
                SIP.package(path)
                print ("SIP " + SIP.bagID + " created.")
                
                SIP.bag.info["Accession-Identifier"] = accessionID
                SIP.bag.info["ArchivesSpace-URI"] = accessionObject["uri"]
                SIP.bag.info["Records-Creator"] = creator
                SIP.bag.info["Content-Description"] = description
                if "condition_description" in accessionObject.keys():
                    SIP.bag.info["Condition-Description"] = accessionObject["condition_description"]
                if "provenance" in accessionObject.keys():
                    SIP.bag.info["Provenance"] = accessionObject["provenance"]
                if "general_note" in accessionObject.keys():
                    SIP.bag.info["General-Note"] = accessionObject["general_note"]
                SIP.bag.info["Source-Location"] = path
                SIP.bag.info["Transfer-Method"] = "https://github.com/UAlbanyArchives/ingest-processing-workflow/ingest.py"
                                    
        
    print ("Writing checksums...")
    SIP.bag.save(manifests=True)
    print ("SIP Saved!")
    
    # List files in txt for processing
    print ("Listing files for processing...")
    listFiles(ID)    
    
    if accession == None:
        SIP.extentLog("/media/SPE/DigitizationExtentTracker/DigitizationExtentTracker.xlsx")
        print ("Logged ingest to DigitizationExtentTracker.")
    else:
        print ("Updating accession " + accessionID)
        if "disposition" in accessionObject.keys():
            accessionObject["disposition"] = accessionObject["disposition"] + "\n" + str(SIP.bagID)
        else:
            accessionObject["disposition"] = str(SIP.bagID)
        
        totalSize = SIP.size()
        inclusiveDates = SIP.dates()
        extent = {"jsonmodel_type":"extent", "portion":"whole","number":str(totalSize[0]),"extent_type":str(totalSize[1])}
        extentFiles = {"jsonmodel_type":"extent", "portion":"whole","number":str(totalSize[2]),"extent_type":"Digital Files"}
        if inclusiveDates[0] == inclusiveDates[1]:
            date = {"jsonmodel_type":"date","date_type":"inclusive","label":"creation","begin":inclusiveDates[0],"expression":inclusiveDates[0]}
        else:
            date = {"jsonmodel_type":"date","date_type":"inclusive","label":"creation","begin":inclusiveDates[0],"end":inclusiveDates[1]}
        if "extents" in accessionObject.keys():
            accessionObject["extents"].append(extent)
            accessionObject["extents"].append(extentFiles)
        else:
            accessionObject["extents"] = [extent, extentFiles]
        accessionObject["dates"].append(date)
            
        updateAccession = client.post(accessionObject["uri"], json=accessionObject)
        if updateAccession.status_code == 200:
            print ("\tSuccessfully updated accession " + accessionID)
        else:
            print (updateAccession.text)
            print ("\tERROR " + str(updateAccession.status_code) + "! Failed to update accession: " + accessionID)
    
    return SIP


# for running with command line args
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("ID", help="Collection ID for the files you are packaging.")
    parser.add_argument("-p", "--path", help="Path of files to ingest. Folder will be removed afterwords.", default=None)
    parser.add_argument("-a", "--accession", help="Optional ArchivesSpace Accession ID for new acquisitions.", default=None)
    args = parser.parse_args()
    
    main(args.ID, args.path, args.accession)
    
