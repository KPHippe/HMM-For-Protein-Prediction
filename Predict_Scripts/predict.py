import re
import os
import sys
import math
import pickle
import copy
import numpy as np
from os.path import join
from operator import itemgetter
from multiprocessing import Process, Queue
from concurrent.futures import ProcessPoolExecutor


import Predict.readSelected as readSelected
import Predict.convertData as convertData


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
    goTERM_to_ID =  readSelected.establishGOIDtoTermRelations("./RequiredResources/")[1]

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
        with open(join(pathToTest, fileName), "r") as f:
            for protID, sequence in readSelected.readFasta(f):
                dataToTest[protID] = convertData.augmentDataToHMMForm([sequence])


        with open(join(pathToOutput,  "CaoLabs2_1_" + speciesName + "_go.txt"), 'a+') as f:
            f.write("AUTHOR\tCaoLabs2\n")
            f.write("MODEL\t1\n")
            f.write("KEYWORDS\thidden Markov model, machine learning\n")

        # multiprocessing to generate all the scores for each sequence
        # futureList = []
        # with ProcessPoolExecutor() as executor:
        #     for protID, sequence in dataToTest.items():
        #         futureList.append(executor.submit(generateScores, protID, sequence, goTERM_to_ID, models))
        #
        # for future in futureList:
        #     protID, sortedScores = future.result()
        #     writeResultsToFile(protID, sortedScores, goTERM_to_ID, pathToOutput, speciesName)

        for protID, sequence in dataToTest.items():
            id, sortedScores = generateScores(protID, sequence, goTERM_to_ID, models)

            writeResultsToFile(protID, sortedScores, goTERM_to_ID, pathToOutput, speciesName)

        '''Terminate the file with END keyword'''
        with open(join(pathToOutput,  "CaoLabs2_1_" + speciesName + "_go.txt"), 'a+') as f:
            f.write("END")
        print(f"Made {fileName} predictions")


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
        model = pickle.load(open(join(pathToModels, fileName), 'rb'))
        models[goTermName] = model

    return models

def score_individual_model(label, model, sequence):
    # print(f"Running {label} model")
    dataToFeedIntoHMM = copy.deepcopy(sequence)

    dataToFeedIntoHMM = np.array(dataToFeedIntoHMM)
    dataToFeedIntoHMM = dataToFeedIntoHMM.astype(np.float64)
    dataToFeedIntoHMM = np.reshape(dataToFeedIntoHMM, (-1,1))


    score = model.score(dataToFeedIntoHMM)
    return (label, score)

def consumer(inQ, outQ):
    while True:
        try:
            # get a new message (the data)
            input_data = inQ.get()

            # this is the 'TERM' signal
            if input_data is None:
                break;

            # unpack the message
            label = input_data[0]
            model = input_data[1]
            sequence = input_data[2]


            # process the data
            label, score = score_individual_model(label, model, sequence)

            # send the  results
            outQ.put( (label, score) )


        except Exception as e:
            print("error!", e)
            break

def distribute_model_tasks(models, sequence, inQ, outQ):
    #send data to workers
    for label, model in models.items():
        model_copy_of_sequence = copy.deepcopy(sequence)
        inQ.put((label, model, model_copy_of_sequence))

    #process results
    scores = {}
    for i in range(len(models)):
        process_return = outQ.get()
        label = process_return[0]
        score = process_return[1]
        scores[label] = score

    return scores


def generateScores(protID, sequence, goTERM_to_ID, models):
    #key -> gotermfilename from test data
    #value -> score
    print(f"sequence ID being tested: {protID}")
    scores = {}

    # '''Original method'''
    # for label, model in models.items():
    #     dataToFeedIntoHMM = copy.deepcopy(sequence)
    #
    #     dataToFeedIntoHMM = np.array(dataToFeedIntoHMM)
    #     dataToFeedIntoHMM = dataToFeedIntoHMM.astype(np.float64)
    #     dataToFeedIntoHMM = np.reshape(dataToFeedIntoHMM, (-1,1))
    #
    #
    #     score = model.score(dataToFeedIntoHMM)
    #
    #     scores[label] = score

    #process and queue
    jobs = 4
    inQ = Queue()
    outQ = Queue()

    workers = [Process(target=consumer,args=(inQ,outQ)) for i in range(jobs)]

    for w in workers:
        w.start()

    scores = distribute_model_tasks(models, sequence, inQ, outQ)

    for i in range(jobs):
        inQ.put(None)
    # join on the workers
    for w in workers:
        w.join()


    sortedScores = [(label, score) for label, score in sorted(scores.items(), key=itemgetter(1), reverse=True)]
    '''Return result so queue can write it all to file'''
    return (protID, sortedScores)


def writeResultsToFile(protID, scores, goTerm_to_ID, pathToOutput, speciesName):
    maxScore = scores[0][1]
    minScore = scores[200][1]


    '''score = 1 - percent difference of score to range'''
    with open( join(pathToOutput, "CaoLabs2_1_" + speciesName + "_go.txt"), 'a+') as f:
        for goTerm,score in scores[:75]:
            probScore = 1.0 - abs(((score - maxScore)/abs(maxScore)))
            writtenScore = "{:0.2f}".format(probScore)
            f.write(f"{protID[1:].split()[0]}\t{goTerm_to_ID[goTerm]}\t{writtenScore}")
            f.write("\n")



if __name__ == "__main__":

    predict(sys.argv[1],sys.argv[2], sys.argv[3])
    sys.exit()
