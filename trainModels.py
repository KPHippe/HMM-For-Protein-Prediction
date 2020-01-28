import os
import sys
from hmmlearn import hmm
import pickle
from tqdm import tqdm
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Pool
import shutil
#to time the different methods
import timeit
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
    #i = 0
    print("Training with no optimization")
    for filename in tqdm(trainingDataList):
        HMMTrain(filename)
        #if i > 100:
        #    sys.exit()
        #i+=1

'''
This is the multiprocessed version of tranModels
'''
def trainModelsProcessPool():
    #leave one full core for other things 
    numCPUs = os.cpu_count() - 2
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
    
    
    #train models concurrently here
    print("Training with ProcessPoolExecutor...") 
    with ProcessPoolExecutor(max_workers=numCPUs) as executor:
        executor.map(HMMTrain, trainingDataList)

        '''Old stuff to try to get tqdm to work'''
        #futures = [executor.submit(HMMTrain, filename) for filename in trainingDataList] 
        
        #kwargs = {
        #    'total': len(futures),
        #    'unit': 'it',
        #    'unit_scale': True,
        #    'leave': True
        #}

        #tqdm stuff here
        #for f in tqdm(as_completed(futures), **kwargs):
        #    pbar.update(1)    

       
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
    #pbar = tqdm(total=len(trainingDataList))
    #execute trianing here
    #p.map(HMMTrain, trainingDataList) #works but not quite what I want
    print("Training using multiprocessing...")
    list(tqdm(p.imap_unordered(HMMTrain, trainingDataList), total=len(trainingDataList)))

    p.close()
    p.join()
    pbar.close() 
    

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
    
    #pbar.update(1)


if __name__ == "__main__":

    try: 
        shutil.rmtree(os.pardir + "/HMMModels/")
    except: 
        pass
    #time all the different methods
    print("ProcessPool: {}".format(timeit.timeit(trainModelsProcessPool, number=1)))
    try: 
        shutil.rmtree(os.pardir + "/HMMModels/")
    except: 
        pass
    
    print("Multiprocessing: {}".format(timeit.timeit(trainModelsMultiprocessing, number=1)))
   
    try: 
        shutil.rmtree(os.pardir + "/HMMModels/")
    except: 
        pass
    
    print("Linear: {}".format(timeit.timeit(trainModels, number=1)))



    
    
