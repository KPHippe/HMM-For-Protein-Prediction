import parseData
import convertData
import trainModels

import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import random
from tqdm import tqdm


def main():

    if not os.path.isdir(os.pardir + "/TrainingDataForHMM") and not os.path.isdir(os.pardir +
            "/TestDataForHMM"):

        GO_TERM_LISTS = parseData.parse()

        GO_TERM_LISTS_80 = GO_TERM_LISTS[0]

        GO_TERM_LISTS_20 = GO_TERM_LISTS[1]

        '''

        create all the files

        '''
        convertData.convertData(GO_TERM_LISTS_80, GO_TERM_LISTS_20)
        
    '''
    
    file that trains everything here

    '''
    #only trains 100 models right now, can train all later
    trainModels.trainModels()
    sys.exit()
    '''
    
    something that predicts here

    '''

#this is for the predictions, not working yet, main only works up until trainmodels
def getTestSequences():
    
    try:
        testingDataList = os.listdir(os.pardir + '/TrainingDataForHMM')
    except:
        print("Training data not present, please run parse data and convert data to create data")
        sys.exit(0)


    
    testSequences = OrderedDict()
    for filename in testingDataList: 
        with open(os.pardir + "/TestDataForHMM/" + filename, "r") as f:
            sequences = f.read().split('\n')
        
        dataForHMM = np.array([]) 
        lengths = [] 

        for sequence in sequences[:-1]:
            tmpList = sequence.split('-')
            for i in range(len(tmpList)):
                tmpList[i] = int(tmpList[i])
            
            testSequences[filename] = tmpList
            lengths.append(len(tmpList))

        dataForHMM = dataForHMM.astype(np.float64)
        dataForHMM = np.reshape(dataForHMM, (-1, 1))





if __name__ == '__main__':
    main()
