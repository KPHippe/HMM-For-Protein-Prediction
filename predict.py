import sys
import os
import re
import pickle
from collections import OrderedDict
import numpy as np
import copy

import readSelected
import convertData
def loadModels():
    '''
    Key -> model name
    value -> model
    '''
    models = {}
    modelFiles = []
   
    #MAKE SURE TO CHANGE BACK TO HMMModels ONCE DEMO DONE
    try:
        modelFiles = os.listdir(os.pardir + "/DEMOMODELS/3DegreeModels")
    except: 
        print("HMMModels folder does not exist")
        sys.exit()

    #print(','.join(modelFiles))
    
    for fileName in modelFiles:
        goTermName = fileName.split('.')[0]
        #MAKE SURE TO CHANGE BACK TO HMMModels ONCE DEMO DONE
        model = pickle.load(open(os.pardir + "/DEMOMODELS/3DegreeModels/" + fileName, 'rb'))
        models[goTermName] = model

    #for term, model in models.items():
    #    print("{}, and has model: {}".format(term, model != None))

    return models

def predict(sequences):
    models = loadModels()
    
    #for sequence in sequences: 
    #    print(sequence)
    #print(len(models))
     
    '''
    Load test data
    '''
    #returns a dict key -> sequence id value -> sequence
    selected10Fasta = readSelected.readFasta(os.pardir + "/PackageStudent/data/Selected10Data/")
    dataToTest = {}
    for protID, sequence in selected10Fasta.items():
        dataToTest[protID] = convertData.augmentDataToHMMForm([sequence])


    #dataToTest = OrderedDict()
    #for fileName in sequences:
    #    #load the sequence and change it into a list
    #    goTerm = fileName.split(".")[0]
    #    rawData = open(os.pardir + "/TestDataForHMM/" + fileName, "r").read().split('\n')
    #    #limit raw data to only have 1 index, remove later
    #    rawData = rawData[0:1]
    #    #print(rawData)
        
        
    #    for sequence in rawData:
    #        sequence = sequence.split("-")
    #        if dataToTest.get(goTerm) != None:
    #            dataToTest[goTerm].append([int(i) for i in sequence])
    #        else:
    #            dataToTest[goTerm] = ([int(i) for i in sequence])

    '''
    Run our seqeunces through the model
    '''
    #THIS IS TEMPORARY FOR THE DEMO
    dict_of_protID_and_goTerm = readSelected.getSelectedGroundTruths(os.pardir +"/PackageStudent/data/Selected10Data/groundtruth/")
    goTERM_to_ID =  readSelected.establishGOIDtoTermRelations(os.pardir +"/functionResource/data/")[1] 

    for protID, sequence in (dataToTest.items()):
        #key -> gotermfilename from test data
        #value -> score

        scores = OrderedDict()

        for label, model in models.items():
            dataToFeedIntoHMM = copy.deepcopy(sequence) 
            
            dataToFeedIntoHMM = np.array(dataToFeedIntoHMM)
            dataToFeedIntoHMM = dataToFeedIntoHMM.astype(np.float64)
            dataToFeedIntoHMM = np.reshape(dataToFeedIntoHMM, (-1,1))


            score = model.score(dataToFeedIntoHMM)

            scores[label] = score

        print("*"*40)
        print("Twe are testing {} from testing label".format(protID))
        print("sequence go IDS {}".format([pID for pID in
            dict_of_protID_and_goTerm[protID[1:]]]))
        sortedScores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        for label, score in sortedScores[:25]:
            print("{} score: {}".format(goTERM_to_ID[label], score))
            if label == protID:
                print('-'*30)
        print("*"*40)

    '''
    Save some results to file same format as CaoSelectedData

    '''

    #for term, sequence in dataToTest.items():
    #    #start working on scores here
    #    #key -> goterm
    #    #value -> score given by model
    #    scores = OrderedDict()
    #    for label, model in models.items():
    #        sequence = [sequence]
    #        sequence = np.array([sequence])
    #        sequence = np.reshape(-1,1)
    #        print("sequence:")
    #        print(sequence)
    #        scores[label] = model.score(sequence)
        
        
    #    print("Original term {}".format(term))
    #    for goTerm, score in scores.items():
    #        print("Model {} score: {}".format(goTerm, score))




if __name__ == "__main__":
    
    predict(None)
    sys.exit()
    
    
    testSequencesFileNames = []
    testSequences = {} 

    try:
        testSequencesFileNames = os.listdir(os.pardir + "/TestDataForHMM")
    except: 
        print("No testing data found... Aborting...")
        sys.exit()
    
    
    predict(testSequencesFileNames)
    sys.exit()

    '''
    This is for testing on our 11 models we have already trainedi
    NO CJEE, NO RX0 
    '''
    shitToPassToPredict = [
            "BIUL.txt",
            "BWME.txt",
            "BWON.txt",
            "CHTZ.txt",
            "CTIR.txt",
            "CUJC.txt",
            "CXGV.txt",
            "MRH.txt",
            "YNZ.txt"
        ]

    trainedExamplesNames = [] 
    #try:
    #    trainedExamplesNames = os.listdir(os.pardir + "/HMMModels")
    #except: 
    #    print("No models found... Aborting...")
    #    sys.exit()
    
    #for fileName in trainedExamplesNames:
    #    name = filename.split('.')[0]

        



    #for i in range(5):
    #    fileName = testSequencesFileNames[i]
    #    sequence = open(os.pardir + "/TestDataForHMM/" + fileName, "r").read().split("-")
    #    term = filename.split(".")[0]

    #    testSequences[term] = seqeunce
    



    predict(shitToPassToPredict)
    sys.exit()
