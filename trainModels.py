import os
import sys
from hmmlearn import hmm
import pickle
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Pool
import shutil
def trainModels():

    try:
        trainingDataList = os.listdir(os.pardir + '/TrainingDataForHMM')
    except:
        print("Training data not present, please run parse data and convert data to create data")
        sys.exit(0)


    '''
    # Making new folder for models
    '''
    try:
        os.mkdir(os.pardir + "/HMMModels/")
    except:
        print("HMMModels folder already made")


    #train models here

    print("Training with no optimization")
    for filename in tqdm(trainingDataList):
        HMMTrain(filename)


'''
This is the multiprocessed version of tranModels
'''
def trainModelsProcessPool(path_to_training_file, path_to_model_save):
    #leave one full core for other things
    numCPUs = os.cpu_count() - 2

    trainingDataList = os.listdir(path_to_training_file)
    pathsLists = [path_to_training_file] *len(trainingDataList)
    outPutPathList = [path_to_model_save] * len(trainingDataList)

    '''
    # Making new folder for models
    '''
    try:
        os.mkdir(path_to_model_save)
    except:
        print(f"{path_to_model_save} already made...")

    #train models concurrently here
    print("Training with ProcessPoolExecutor...")
    with ProcessPoolExecutor(max_workers=numCPUs) as executor:
        executor.map(HMMTrain, trainingDataList, pathsLists, outPutPathList)

'''
This is the multiprocessed version of tranModels
'''
def trainModelsMultiprocessing():
    '''Setup multiprocessing'''
    #leave one full core for other things
    numCPUs = os.cpu_count() - 2
    p = Pool(numCPUs)

    try:
        trainingDataList = os.listdir(os.pardir + '/TrainingDataForHMM')
    except:
        print("Training data not present, please run parse data and convert data to create data")
        sys.exit(0)


    '''
    # Making new folder for models
    '''
    try:
        os.mkdir(os.pardir + "/HMMModels/")
    except:
        print("HMMModels folder already made")


    '''train models concurrently here'''
    '''
    Example:
    list(tqdm.tqdm(pool.imap_unordered(do_work, range(num_tasks)), total=len(values)))
    '''

    print("Training using multiprocessing...")

    list(tqdm(p.imap_unordered(HMMTrain, trainingDataList),
        total=len(trainingDataList)))

    p.close()
    p.join()



def HMMTrain(filename, path_to_training_file, path_to_model_save):
    #parse the data
    '''
    model in '1-2-3-...-27' form

    '''
    with open(path_to_training_file + filename, "r") as f:
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
    model = hmm.GaussianHMM(n_components=5, covariance_type='full', tol=0.001, n_iter=1000)
    model.fit(dataForHMM, lengths)

    #pickle the model
    modelName = filename.split('.')[0] + ".mdl"
    with open(path_to_model_save + modelName, 'wb') as f:
        pickle.dump(model, f)

    print(f"{modelName} model made")
