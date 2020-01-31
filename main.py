import parseData
import convertData
import trainModels
import predict

import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import random
from tqdm import tqdm


def main(args):
    '''
    --predict 
    #other args
    1 -> path to test sequences
    2 -> path to models 
    3 -> path to output texts
    --generateData
    #not working yet 
    --train
    #not working yet 

    '''

    '''This is for sys.args processing'''
    if("--predict") in args:
        '''
        Predict needs path to test sequences, path to models, path to output
        '''
        try: 
            os.path.isdir(args[1])
            os.path.isdir(args[2])
            os.path.isdir(args[3])
        except: 
            print("A folder does not exist/is not a valid path\nPlease enter a valid path")
            sys.exit()

        predict.predict(args[1], args[2], args[3])
    '''This ends sys.args processing'''
    

    


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
    
    Train all the models here

    '''

    trainModels.trainModelsProcessPool()

    '''
    
    Prediction calculations here

    '''
    predict.predict(args[1], args[2], args[3])




if __name__ == '__main__':
    main(sys.argv[1:])
