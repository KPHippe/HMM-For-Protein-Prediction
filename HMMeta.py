import Augment_Scripts.parseData as parseData
import Augment_Scripts.convertData as convertData
from Train_Scripts.trainModels import trainModelsProcessPool
import Predict_Scripts.predict as predict

import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import random

from timeit import default_timer as timer

def main(args):
    '''
    --predict
        1 -> path to test sequences
        2 -> path to models
        3 -> path to output texts
    --generateData
    #not working yet
    --train
    #not working yet

    '''

    '''
    This is for sys.args processing
    '''
    if("--predict") in args:
        '''
        Predict needs path to test sequences, path to models, path to output
        '''
        start = timer()
        try:
            # Main will truncate original command line arguments. will remove "python"
            os.path.isdir(args[1])
            os.path.isdir(args[2])
            os.path.isdir(args[3])
        except:
            print("A folder does not exist/is not a valid path\nPlease enter a valid path")
            sys.exit()

        predict.predict(args[1], args[2], args[3])
        print("Predictions made...")
        total_t = timer() - start
        print(f"Total time: {total_t}")
        sys.exit()

    if("--train") in args:

        """
        Train requires a path to the training file,
        and a path for the output.
        """
        try:
            os.path.isdir(args[1])
            os.path.isdir(args[2])
        except:
            print("--train requires 2 arguments, first is path_to_training_file\nSecond is path_FOR_model_output")
            sys.exit()

        trainModelsProcessPool(args[1], args[2])
        print(f"Models saved to {args[2]}")
        sys.exit()
    """
    Argument order is /pathToInput, pathToTrainingData, pathtotesting
    """
    if("--make") in args:
        try:
            # Main will truncate original command line arguments. will remove "python"
            os.path.isdir(args[1])
            os.path.isdir(args[2])
            os.path.isdir(args[3])
        except:
            print("--make requires these three arguments:\nA path_to_input_data, a path_to_training_data, a path_to_testing_data")
            sys.exit()
        #do the making of data here
        parseData.parse(args[1], args[2], args[3]) #list of two dictionaries, 80 first, 20 second

        print("Done making data...")
        sys.exit()

    if("--all") in args:
        are_you_sure = input(print("Creating everything from scratch, are you sure? [Y/N]"))
        if (are_you_sure in "yY"):
            # parseData needs (pathToData, pathTo)
            parseData.parse(os.pardir + "/requiredResource/New_filtered_balanced_protein_language_data_34567_top2000", os.pardir + "/requiredResource/", os.pardir + "/requiredResource/")
            trainModels.trainModelsProcessPool(os.pardir + "/requiredResource/", os.pardir + "requiredResource/")
            predict.predict(os.pardir + "/requiredResource/TestDataForHMM", os.pardir + "/requiredResource/HMMModels", os.pardir + "/requiredResource/selected.fasta")
        else:
            print("Smart move, stopping everything now.")
            sys.exit()




if __name__ == '__main__':
    main(sys.argv[1:])
