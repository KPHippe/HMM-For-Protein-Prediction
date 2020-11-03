import os
import sys
import shutil


'''Takes in path to models folder and path to training folder, removes any training data that
already had a model'''
def determineModelsToTrain(args):

    modelsMade = []
    trainingData = []
    try:
        modelsMade = os.listdir(args[0])
    except:
        print(f"{args[0]} does not exist...")
        sys.exit()
    
    try:
        trainingData  = os.listdir(args[1])
    except: 
        print(f"{args[1]} does not exist...")
        sys.exit()

    filesRemoved = 0
    for modelFile in modelsMade:
        modelTXTFile = modelFile.split(".")[0] + ".txt"
        if modelTXTFile in trainingData:
            try: 
                os.remove(args[1] + modelTXTFile)
                filesRemoved += 1 
            except:
                print(f"{modelTXTFile} does not exist in training data")

    print(f"Training data updated {filesRemoved} files removed")

     




if __name__ == "__main__":
    determineModelsToTrain(sys.argv[1:])

