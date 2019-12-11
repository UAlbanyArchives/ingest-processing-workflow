import os

def listFiles(ID, verbose=False):

    if os.name == 'nt':
        processingDir = "\\\\Romeo\\SPE\\processing"
    else:
        processingDir = "/media/SPE/processing"

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
        for file in files:
            filePath = os.path.join(root, file).split(derivatives)[1]
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
        for file in files:
            filePath = os.path.join(root, file).split(masters)[1]
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
    #argParse.add_argument("-v", "--verbose", help="lists all files written.", default=False)
    args = argParse.parse_args()
    
    listFiles(args.ID, True)