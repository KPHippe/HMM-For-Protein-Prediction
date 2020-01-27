import os
import sys
from hmmlearn import hmm
import pickle
from tqdm import tqdm
import numpy as np


def trainModels():

    try:
        trainingDataList = os.listdir(os.pardir + '/TrainingDataForHMM')
    except:
        print("Training data not present, please run parse data and convert data to create data")
        sys.exit(0)


    #print(",".join(trainingDataList))
    #print(len(trainingDataList))
    '''
    # Making new folder for models
    '''
    try:
        os.mkdir(os.pardir + "/HMMModels/")
    except:
        print("HMMModels folder already made")
    
    
    #train models here
    i = 0
    for filename in tqdm(trainingDataList):
        HMMTrain(filename)
        if i > 3:
            sys.exit()
        i+=1


def HMMTrain(filename):
    #parse the data
    '''
    model in '1-2-3-...-27' form

    '''
    with open(os.pardir + "/TrainingDataForHMM/" + filename, "r") as f:
        sequences = f.read().split('\n')
    
    dataForHMM = np.array([]) 
    lengths = [] 

    for sequence in sequences[:-1]:
        tmpList = sequence.split('-')
        for i in range(len(tmpList)):
            tmpList[i] = int(tmpList[i])
        
        dataForHMM = np.append(dataForHMM, tmpList)
        lengths.append(len(tmpList))

    dataForHMM = dataForHMM.astype(np.float64)
    dataForHMM = np.reshape(dataForHMM, (-1, 1))


    #train the model

    model = hmm.GaussianHMM(n_components=1, covariance_type='full', n_iter=1000)

    model.fit(dataForHMM, lengths)
    randTest = np.random.rand(dataForHMM.shape[0], dataForHMM.shape[1])
    print("Model: {} dataForHMM score: {} randomData score: {}".format(filename,
        np.expm1(model.score(dataForHMM)),np.expm1(model.score(randTest))))
    
    #pickle the model 
    
    modelName = filename.split('.')[0] + ".mdl"
    with open(os.pardir + "/HMMModels/" + modelName, 'wb') as f:
        pickle.dump(model, f)




if __name__ == "__main__":
    trainModels()



