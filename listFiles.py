import os

def listFiles(ID, directories, verbose=False):

    if os.name == 'nt':
        processingDir = "\\\\Lincoln\\Library\\SPE_Processing\\backlog"
    else:
        processingDir = "/media/Library/SPE_Processing/backlog"

    colID = ID.split("_")[0].split("-")[0]
    package = os.path.join(processingDir, colID, ID)
    derivatives = os.path.join(package, "derivatives")
    masters = os.path.join(package, "masters")

    if not os.path.isdir(package) or not os.path.isdir(derivatives):
        raise ("ERROR: " + package + " is not a valid package.")
        
    # open the output file
    f = open(os.path.join(package, 'derivatives.txt'), 'w')

    #get all files in derivatives folder
    for root, dirs, files in os.walk(derivatives):
        if directories:
            derList = dirs
        else:
            derList = files
        for item in derList:
            filePath = os.path.join(root, item).split(derivatives)[1]
            if filePath.startswith("\\"):
                filePath = filePath[1:]
            if filePath.startswith("/"):
                filePath = filePath[1:]
            if verbose:
                print ("writing " + filePath)
            f.write(filePath + "\n")
            
    # close the output file
    f.close()

    # open the output file
    f = open(os.path.join(package, 'masters.txt'), 'w')

    #get all files in masters folder
    for root, dirs, files in os.walk(masters):
        if directories:
            masList = dirs
        else:
            masList = files
        for item in masList:
            filePath = os.path.join(root, item).split(masters)[1]
            if filePath.startswith("\\"):
                filePath = filePath[1:]
            if filePath.startswith("/"):
                filePath = filePath[1:]
            if verbose:
                print ("writing " + filePath)
            f.write(filePath + "\n")
            
    # close the output file
    f.close()

# for running with command line args
if __name__ == '__main__':
    import argparse

    argParse = argparse.ArgumentParser()
    argParse.add_argument("ID", help="ID for a package in Processing directory.")
    argParse.add_argument("-d", "--directories", help="Only list directories", default=False, action="store_true")
    #argParse.add_argument("-v", "--verbose", help="lists all files written.", default=False)
    args = argParse.parse_args()
    
    listFiles(args.ID, args.directories, True)
