import sys
import os
import re
import pickle
from collections import OrderedDict
import numpy as np
import copy
from concurrent.futures import ProcessPoolExecutor
import math

import readSelected
import convertData
def loadModels(pathToModels):
    '''
    Key -> model name
    value -> model
    '''
    models = {}
    modelFiles = []
   
    try:
        modelFiles = os.listdir(pathToModels)
    except: 
        print(f"{pathToModels} folder does not exist")
        sys.exit()

    
    for fileName in modelFiles:
        goTermName = fileName.split('.')[0]
        model = pickle.load(open(pathToModels + fileName, 'rb'))
        models[goTermName] = model


    return models

def predict(pathToTest, pathToModels, pathToOutput):
    models = loadModels(pathToModels)
    
    testSequenceFileNames = []
    try: 
        testSequenceFileNames = os.listdir(pathToTest)
    except: 
        print(f"Test folder: {pathToTest} not found")
        sys.exit()
    speciesNames = []
    for fileName in testSequenceFileNames:
        speciesNames.append(fileName.split(".")[1])
    print(testSequenceFileNames) 
    print(speciesNames)


    '''
    Run our seqeunces through the model
    '''
        
    '''Change this to be required resource later'''
    goTERM_to_ID =  readSelected.establishGOIDtoTermRelations("/RequiredResources/")[1] 

    '''
    Establish output file with correct header 

    '''
    try: 
        os.mkdir(pathToOutput)
        print(f"{pathToOutput} folder made...")
    except:
        pass

    
    for fileName, speciesName in zip(testSequenceFileNames, speciesNames):
        
        dataToTest = {}
        with open(pathToTest + fileName, "r") as f:
            for protID, sequence in readSelected.readFasta(f):
                dataToTest[protID] = convertData.augmentDataToHMMForm([sequence])


        with open(pathToOutput + "ReshapeYourData_1_" + speciesName + "_go.txt", 'a+') as f: 
            f.write("AUTHOR\tReshapeYourData\n")
            f.write("MODEL\t1\n")
            f.write("KEYWORDS\thidden Markov model, machine learning\n")
        
        #multiprocessing to generate all the scores for each sequence
        futureList = []
        with ProcessPoolExecutor() as executor:
            for protID, sequence in dataToTest.items():
                futureList.append(executor.submit(generateScores, protID, sequence, goTERM_to_ID, models))

        for future in futureList:
            protID, sortedScores = future.result()
            writeResultsToFile(protID, sortedScores, goTERM_to_ID, pathToOutput, speciesName)

        
        '''Terminate the file with END keyword'''
        with open(pathToOutput + "ReshapeYourData_1_" + speciesName + "_go.txt", 'a+') as f: 
            f.write("END")
        print(f"Made {fileName} predictions")


def generateScores(protID, sequence, goTERM_to_ID, models):

    #key -> gotermfilename from test data
    #value -> score
    print(f"sequence ID being tested: {protID}")
    scores = OrderedDict()

    for label, model in models.items():
        dataToFeedIntoHMM = copy.deepcopy(sequence) 
        
        dataToFeedIntoHMM = np.array(dataToFeedIntoHMM)
        dataToFeedIntoHMM = dataToFeedIntoHMM.astype(np.float64)
        dataToFeedIntoHMM = np.reshape(dataToFeedIntoHMM, (-1,1))


        score = model.score(dataToFeedIntoHMM)
        
        scores[label] = score
    
    sortedScores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    '''Return result so queue can write it all to file'''
    return (protID, sortedScores)


def writeResultsToFile(protID, scores, goTerm_to_ID, pathToOutput, speciesName):
    maxScore = scores[0][1]
    minScore = scores[200][1]


    '''score = 1 - percent difference of score to range'''
    with open( pathToOutput + "ReshapeYourData_1_" + speciesName + "_go.txt", 'a+') as f: 
        for goTerm,score in scores[:75]: 
            probScore = 1.0 - abs(((score - maxScore)/abs(maxScore)))
            writtenScore = "{:0.2f}".format(probScore)
            f.write(f"{protID[1:].split()[0]}\t{goTerm_to_ID[goTerm]}\t{writtenScore}")    
            f.write("\n")



if __name__ == "__main__":
    
    predict(sys.argv[1],sys.argv[2], sys.argv[3])
    sys.exit()
    
