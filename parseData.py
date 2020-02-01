import sys
import os
import time
import re
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import random
from tqdm import tqdm 
import itertools

import augmentData
def parse(path_to_input_data, path_to_train_data, path_to_test_data):

    # file_path = os.pardir + "/functionResource/data/New_filtered_balanced_protein_language_data_34567_top2000"
    file_path = path_to_input_data

    '''
    Read in our data, store it in UNIPROT

    data structure
    key: protein sequence -> string
    value: protein structure -> list of strings

    '''

    UNIPROT = OrderedDict()

    raw_data = open(file_path, 'r').read().strip()
    raw_data = re.split('[|]+|\n+', raw_data)


    for i in range(0,len(raw_data), 2):
        sequence = raw_data[i].replace(' ', '')
        function = raw_data[i+1].split(" ")
        UNIPROT[sequence] = function

    print("Done reading data...")

    '''

    Create our random split for training and testing data

    '''
    list_dict_keys = list(UNIPROT.keys())
    random.shuffle(list_dict_keys)
    eightyPercent = list_dict_keys[:round(len(list_dict_keys)*.8)]
    twentyPercent = list_dict_keys[len(eightyPercent):]



    '''
    This function makes a dictionary: 
        key -> GO Term
        value -> list of sequences
    '''
    GOTERMSDICT = {} 

    for sequence in list(UNIPROT.keys()): 
        terms = UNIPROT[sequence]
        for term in terms: 
            if GOTERMSDICT.get(term) != None: 
                GOTERMSDICT.get(term).append(str(sequence))

            else: 
                GOTERMSDICT[term] = []
                GOTERMSDICT[term].append(str(sequence))
    
    # BANNED TERMS HERE!
    bannedTerms = set()
    #bannedTerms.add("PRN")
    #bannedTerms.add("CON")
    #bannedTerms.add("NUL")

    GO_TERM_DICT_80 = OrderedDict()
    GO_TERM_DICT_20 = OrderedDict()

    for sequence in eightyPercent: 
        terms = UNIPROT[sequence]
        for term in terms:
            # TODO 
            # temporairly removed bannedTerms because we have a delimitter on # sequences
            if term not in bannedTerms:

                if GO_TERM_DICT_80.get(term) != None: 
                    GO_TERM_DICT_80.get(term).append(str(sequence))

                else: 
                    GO_TERM_DICT_80[term] = []
                    GO_TERM_DICT_80[term].append(str(sequence))
           
           
    for sequence in twentyPercent: 
        terms = UNIPROT[sequence]
        for term in terms:
            # TODO 
            # temporairly removed bannedTerms because we have a delimitter on # sequences
            if term not in bannedTerms:

                if GO_TERM_DICT_20.get(term) != None: 
                    GO_TERM_DICT_20.get(term).append(str(sequence))

                else: 
                    GO_TERM_DICT_20[term] = []
                    GO_TERM_DICT_20[term].append(str(sequence))
        
    # TODO this is the new GO_TERM_LISTS_80 that has been shuffled and randomly 100 selected
    training_dict_100 = {}
    testing_dict_100 = {}
    
    
    # limit sequences to 100 for each goTerm
    '''
    Try to make it so we don't have to return anything from this function
    Write to files from AugmentData
    '''
    #smallTrainingTuple = list(GO_TERM_DICT_80.items())[:100]
    nList = [100] *len(GO_TERM_DICT_80)
    pathsList = [path_to_train_data] * len(GO_TERM_DICT_80)
    
    #resultingTrainingData = {} # just to test my multiprocessing implementation
    with ProcessPoolExecutor(max_workers=(os.cpu_count() -2)) as executor: 
        #for term, sequences in tqdm(GO_TERM_DICT_80.items()):

        executor.map(multiProcessingAugmentation, GO_TERM_DICT_80.items(), nList, pathsList)
        #futuresList.append(future)

    #print("Augmenting Data...")
    # for future in futuresList:
    #     if future.done():
                
    #         result = future.result()    
    #         training_dict_100[result[0]] = result[1]
    # print(f"Length of training dictionary:  {len(training_dict_100)}")

    for term, sequences in GO_TERM_DICT_20.items():
        if len(sequences) >= 100:
            testing_list_100 = random.sample(sequences, 100)
            #testing_dict_100[term] = testing_list_100
            augmentData.writeToFile(term, testing_list_100, path_to_test_data)
        else:
            # TODO 
            # augmentData.writeToFile
            # if len(sequences) == 1:
            #     properFormatSequence = []
            #     properFormatSequence.append([i for i in sequences])
            #     augmentData.writeToFile(term, properFormatSequence, path_to_test_data)
            # else:

            augmentData.writeToFile(term, sequences, path_to_test_data)
                #testing_dict_100[term] = sequences 
            


def multiProcessingAugmentation(termSequenceTuple, n, path_to_output):

    
    result = None
    term = termSequenceTuple[0]
    sequences = termSequenceTuple[1]
    #print(f"inside augmentMulitProcessing, {term} len sequences: {len(sequences)}, n:{n}, path{path_to_output}")

    #print(f"inside multiProcessingAugmentation term: {term} len of sequences: {len(sequences)}")
    if len(sequences) >= 100:
        training_list_100 = random.sample(sequences, 100)
        result = (term, training_list_100)
        augmentData.writeToFile(result[0], result[1], path_to_output)
    else:
        # TODO 
        """UNCOMMENTTHISLINE TO ENABE AUGMENTDATA TO ACTUALLY RUN"""
        augmentData.augmentData(term, sequences, 100, path_to_output)
        #training_list_100 = sequences
        #result = (term, training_list_100)
        
    #print("returning result from multiprocessingAugmentation in parseData")
    #print(f"result is: {','.join(str(i) for i in result)}")
    #augmentData.writeToFile(term, result, path_to_output)
    #return result



'''
This method will iterate through each GoTerm and for terms that have greater than 100 sequences
will randomly select 100. For GoTerms with less than 100 sequences this method will use an HMM
to create/predict additional sequences (up to the limit 100)
'''
if __name__ == "__main__":

    #parse("","","")
    sys.exit()
