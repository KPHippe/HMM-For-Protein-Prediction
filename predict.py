import sys
import os
import re
import pickle
from collections import OrderedDict
import numpy as np
import copy

import readSelected
import convertData
def loadModels(pathToModels):
    '''
    Key -> model name
    value -> model
    '''
    models = {}
    modelFiles = []
   
    #MAKE SURE TO CHANGE BACK TO HMMModels ONCE DEMO DONE
    try:
        modelFiles = os.listdir(pathToModels)
    except: 
        print("HMMModels folder does not exist")
        sys.exit()

    #print(','.join(modelFiles))
    
    for fileName in modelFiles:
        goTermName = fileName.split('.')[0]
        model = pickle.load(open(pathToModels + fileName, 'rb'))
        models[goTermName] = model


    return models

def predict(pathToTest, pathToModels, pathToOutput):
    models = loadModels(pathToModels)
    
     
    '''
    Load test data
    '''
    #returns a dict key -> sequence id value -> sequence
    selected10Fasta = readSelected.readFasta(pathToTest)
    dataToTest = {}
    for protID, sequence in selected10Fasta.items():
        dataToTest[protID] = convertData.augmentDataToHMMForm([sequence])



    '''
    Run our seqeunces through the model
    '''
    #THIS IS TEMPORARY FOR THE DEMO
    try: 
        dict_of_protID_and_goTerm = readSelected.getSelectedGroundTruths(os.pardir+"/Competition50Targets/groundtruth/")
    except: 
        print("No ground truths found...")
    

    goTERM_to_ID =  readSelected.establishGOIDtoTermRelations(os.pardir +"/functionResource/data/")[1] 

    '''
    Establish output file with correct header 

    '''
    try: 
        os.mkdir(pathToOutput.split(":")[0] +"/")
    except: 
        print(f"{pathToOutput} folder already made...")

    with open(pathToOutput.split(":")[0] + "/" + pathToOutput.split(":")[1], 'a+') as f: 
        f.write("AUTHOR\tTeam Reshape Your Data\n")
        f.write("MODEL\tHidden Markov Model\n")
        f.write("KEYWORDS\tHidden Markov Model, machine learning\n")
        f.write("Sequence\tGO ID's\tConfidence\n")

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
            randData = np.random.rand(dataToFeedIntoHMM.shape[0], dataToFeedIntoHMM.shape[1])
            randScore = model.score(randData)
            scores[label] = (score, randScore)
        
        sortedScores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        '''Save Results to file'''
        writeResultsToFile(protID, sortedScores, goTERM_to_ID, pathToOutput) 

        print("*"*40)
        print("We are testing {} from CompetitoinTargets".format(protID[1:]))
        try: 
            print("sequence go IDS {}".format([pID for pID in dict_of_protID_and_goTerm[protID[1:]]]))
        except: 
            pass
        for label, scores in sortedScores[:25]:
            print("{} score: {} randomSequence score: {}".format(goTERM_to_ID[label], scores[0], scores[1]))
            if label == protID:
                print('-'*30)
        print("*"*40)

    '''Terminate the file with END keyword'''
    with open(pathToOutput.split(":")[0] + "/" + pathToOutput.split(":")[1], 'a+') as f: 
        f.write("END")



def writeResultsToFile(protID, scores, goTerm_to_ID, pathToOutput):
     
    try:

        fileName = pathToOutput.split(":")[1]
    except:
        print("Invalid output file path, or name...")
        sys.exit()
    try: 
        os.mkdir(pathToOutput.split(":")[0] +"/")
    except: 
        print(f"{pathToOutput} folder already made...")

    
    with open(pathToOutput.split(":")[0] + "/" + fileName, 'a+') as f: 
        for goTerm,score in scores[:1000]: 
            f.write(f"{protID[1:]}\t{goTerm_to_ID[goTerm]}\t{str(score[0])}")    
            f.write("\n")



if __name__ == "__main__":
    
    predict(sys.argv[1],sys.argv[2], sys.argv[3])
    sys.exit()
    