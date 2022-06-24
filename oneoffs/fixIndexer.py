import json
from asnake.aspace import ASpace

aspace = ASpace()
repo = aspace.repositories(2)

collection = repo.resources(171)

print (collection.title)

for child in collection.tree.children:
    print (child.title)
    
    q = child.title
    r = aspace.client.get("repositories/2/search?page=1&aq={\"query\":{\"field\":\"title\", \"value\":\"" + q + "\", \"jsonmodel_type\":\"field_query\"}}")

    count = len(r.json()["results"])
    print ("\t" + str(count))
    
    for folder in child.children:
        
        
        #if ";" in folder.title:
        #    print ("!!!")
        #if "\"" in folder.title:
        #    print ("!!!")
        q = folder.title.replace(";", "").replace("\"", "").replace("?", "")
        r = aspace.client.get("repositories/2/search?page=1&aq={\"query\":{\"field\":\"title\", \"value\":\"" + q + "\", \"jsonmodel_type\":\"field_query\"}}")

        
        count = len(r.json()["results"])
        if count == 0:
            print ("\t" + folder.title)
            print ("\t\t" + str(count))
            
            print (folder.record_uri)
            
            #fix = aspace.client.get(folder.record_uri).json()
            #fix["title"] = fix["title"].strip()
            
            #p = aspace.client.post(fix["uri"], json=fix)
            #print (p.status_code)
            
            