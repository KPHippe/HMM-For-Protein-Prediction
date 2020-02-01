import sys
import os
import time
import re
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import random
from tqdm import tqdm 

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
    futuresList = []
    #resultingTrainingData = {} # just to test my multiprocessing implementation
    with ProcessPoolExecutor(max_workers=(os.cpu_count() -2)) as executor: 
        for term, sequences in tqdm(GO_TERM_DICT_80.items()):
            future = executor.submit(multiProcessingAugmentation, term, sequences)
            futuresList.append(future)

    print("Augmenting Data...")
    for future in futuresList:
        if future.done():
                
            result = future.result()    
            training_dict_100[result[0]] = result[1]
    print(f"Length of training dictionary:  {len(training_dict_100)}")

    for term, sequences in GO_TERM_DICT_20.items():
        if len(sequences) >= 100:
            testing_list_100 = random.sample(sequences, 100)
            testing_dict_100[term] = testing_list_100
        else:
            # TODO 
            # augmentData()
            testing_dict_100[term] = sequences 
            



    # print("Done with parseData, writing files to locations...")
    # # UPDATE WITH INCREASE IN SEQUQNCES PER GO TERM. 100 REPRESENTS 100 SEQ
    # train_file = open(path_to_train_data, "w")
    # train_file.writelines(training_dict_100)
    # train_file.close()

    # testing_file = open(path_to_test_data, "w")
    # testing_file.writelines(testing_dict_100)
    # train_file.close()

    return (training_dict_100, testing_dict_100)

def multiProcessingAugmentation(term, sequences):
    #print(f"inside augmentMulitProcessing, {term} len sequences: {len(sequences)}")
    result = None
    #print(f"inside multiProcessingAugmentation term: {term} len of sequences: {len(sequences)}")
    if len(sequences) >= 100:
        training_list_100 = random.sample(sequences, 100)
        result = (term, training_list_100)
    else:
        # TODO 
        """UNCOMMENTTHISLINE TO ENABE AUGMENTDATA TO ACTUALLY RUN"""
        training_list_100 = augmentData.augmentData(sequences, 100)
        #training_list_100 = sequences
        result = (term, training_list_100)
    print(f"result is: {','.join(str(i) for i in result)}")
    return result



'''
This method will iterate through each GoTerm and for terms that have greater than 100 sequences
will randomly select 100. For GoTerms with less than 100 sequences this method will use an HMM
to create/predict additional sequences (up to the limit 100)
'''
if __name__ == "__main__":

    #parse("","","")
    sys.exit()
