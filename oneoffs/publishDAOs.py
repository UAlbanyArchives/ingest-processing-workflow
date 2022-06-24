from asnake.aspace import ASpace

aspace = ASpace()
repo = aspace.repositories(2)

count = 0
unpublished = 0
unlinked = 0

collections = {}

#dao = repo.digital_objects(15784)
#dao = repo.digital_objects(32006)
#print (dao)
#object = aspace.client.get(dao.linked_instances[0].ref).json()
#resource = aspace.client.get(object["resource"]["ref"]).json()
#print (resource["title"])
#print (len(dao.linked_instances))

def fix(dao, resource):
    #if resource["title"] == "The State College Echo Collection":
    if "Student Success Stories Podcasts" in resource["title"]:
        print ("Fixing " + dao.uri + "...")
        daoJSON = dao.json()
        daoJSON["publish"] = True
        r = aspace.client.post(dao.uri, json=daoJSON)
        print ("\t--> " + str(r.status_code))



for dao in repo.digital_objects:
    count += 1
    if len(dao.linked_instances) < 1:
        unlinked += 1
        delete = aspace.client.delete(dao.uri)
        print (delete.status_code)
    else:
        if "publish" in dir(dao):
            if dao.publish == False:
                unpublished += 1
                object = aspace.client.get(dao.linked_instances[0].ref).json()
                resource = aspace.client.get(object["resource"]["ref"]).json()
                title = resource["title"]
                if title in collections.keys():
                    collections[title] += 1
                else:
                    collections[title] = 1
                if dao.title.endswith(".msg"):
                    pass
                else:
                    print (resource["title"])
                    print ("\t" + dao.uri)
                    print ("\t" + dao.title)
                    #fix(dao, resource)
                
                
        else:
            unpublished += 1
            object = aspace.client.get(dao.linked_instances[0].ref).json()
            resource = aspace.client.get(object["resource"]["ref"]).json()
            title = resource["title"]
            if title in collections.keys():
                collections[title] += 1
            else:
                collections[title] = 1
            if dao.title.endswith(".msg"):
                pass
            else:
                print (resource["title"])
                print ("\t" + dao.uri)
                print ("\t" + dao.title)
                #fix(dao, resource)
            

print (unlinked)
print (unpublished)
print (count)
print (collections)
