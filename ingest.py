import os
import sys
import json
import bagit
import argparse

from packages import SubmissionInformationPackage

#version of ingest.py
version = "0.1"
defaultPath = "/media/SPE/ingest"

parser = argparse.ArgumentParser()
parser.add_argument("ID", help="Collection ID for the files you are packaging")
parser.add_argument("-p", "--path", help="Path of files to ingest. Folder will be removed afterwords", default=None)
parser.add_argument("-a", "--accession", help="Optional ArchivesSpace Accession ID for new acquisisions.", default=None)
args = parser.parse_args()

if args.path:
    if os.path.isdir(args.path):
        path = args.path
    else:
        raise Exception("ERROR: " + str(args.path) + " is not a valid path.")
else:
    if not os.path.isdir(defaultPath):
        os.mkdir(defaultPath)
    path = os.path.join(defaultPath, args.ID)
    if not os.path.isdir(path):
        raise Exception("ERROR: no " + args.ID + " directory exists for ingest in " + defaultPath)
print ("Reading " + path)
    
        
if not args.accession:
    print ("Building SIP...")
    SIP = SubmissionInformationPackage(args.ID)
    SIP.package(path)
    print ("SIP " + SIP.bagID + " created.")

else:
    print ("Reading accession " + str(args.accession))
    import asnake.logging as logging
    from asnake.client import ASnakeClient
    client = ASnakeClient()
    client.authorize()

    logging.setup_logging(stream=sys.stdout, level='INFO')
    
    call = "repositories/2/search?page=1&aq={\"query\":{\"field\":\"identifier\", \"value\":\"" + str(args.accession) + "\", \"jsonmodel_type\":\"field_query\"}}"
    accessionResponse = client.get(call).json()
    if len(accessionResponse["results"]) < 1:
        raise Exception("ERROR: Could not find accession with ID: " + str(args.accession))
    else:
        accession = json.loads(accessionResponse["results"][0]["json"])
        if "id_1" in accession.keys():
            accessionID = accession["id_0"] + "-" + accession["id_1"]
        if args.accession != accessionID:
            raise Exception("ERROR: Could not find exact accession with ID: " + str(args.accession))
        if not "content_description" in accession.keys():
            raise Exception("ERROR: no content description in " + str(args.accession) + " accession, " + accession["uri"])
        if len(accession["related_resources"]) < 1:
            raise Exception("ERROR: no related resource for " + str(args.accession) + " accession, " + accession["uri"])
        else:
            resource = client.get(accession["related_resources"][0]["ref"]).json()
            creator = resource["title"]
            if not str(args.ID).lower() == resource["id_0"].lower():
                raise Exception("ERROR: accession " + str(args.accession) + " does not link to collection ID " + args.ID + ". Instead linked to " + resource["id_0"])
            description = accession["content_description"]
            
            print ("Building SIP...")
            SIP = SubmissionInformationPackage(args.ID)
            SIP.package(path)
            print ("SIP " + SIP.bagID + " created.")
            
            SIP.bag.info["Accession-Identifier"] = accessionID
            SIP.bag.info["ArchivesSpace-URI"] = accession["uri"]
            SIP.bag.info["Records-Creator"] = creator
            SIP.bag.info["Content-Description"] = description
            if "condition_description" in accession.keys():
                SIP.bag.info["Condition-Description"] = accession["condition_description"]
            if "provenance" in accession.keys():
                SIP.bag.info["Provenance"] = accession["provenance"]
            if "general_note" in accession.keys():
                SIP.bag.info["General-Note"] = accession["general_note"]
            SIP.bag.info["Source-Location"] = path
            SIP.bag.info["Transfer-Method"] = "https://github.com/UAlbanyArchives/ingest-processing-workflow/ingest.py"
            
            print ("Updating accession " + accessionID)
            if "disposition" in accession.keys():
                accession["disposition"] = accession["disposition"] + "\n" + str(SIP.bagID)
            else:
                accession["disposition"] = str(SIP.bagID)
            if "inventory" in accession.keys():
                accession["inventory"] = accession["inventory"] + "\n" + SIP.inventory()
            else:
                accession["inventory"] = SIP.inventory()
                
            totalSize = SIP.size()
            extent = {"jsonmodel_type":"extent", "portion":"whole","number":str(totalSize[0]),"extent_type":str(totalSize[1])}
            if "extents" in accession.keys():
                accession["extents"].append(extent)
            else:
                accession["extents"] = [extent]
                
            updateAccession = client.post(accession["uri"], json=accession)
            if updateAccession.status_code == 200:
                print ("\tSuccessfully updated accession " + accessionID)
            else:
                print ("\tERROR failed to update accession: " + accessionID)
                
    
print ("Writing checksums...")
SIP.bag.save(manifests=True)
print ("SIP Saved!")
    
