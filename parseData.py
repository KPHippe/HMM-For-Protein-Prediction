import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import random
from tqdm import tqdm 

import augmentData
def parse():

    file_path = os.pardir + "/functionResource/data/New_filtered_balanced_protein_language_data_34567_top2000"

    if len(sys.argv) > 1:
        file_path = os.curdir + sys.argv[1]
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
    bannedTerms = set()
    bannedTerms.add("PRN")
    #######
    # might need to ban PRN.txt

    # for term, sequences in GOTERMSLISTS.items():
    #     if len(sequences) > 10000:
    #         bannedTerms.add(term)

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
    for term, sequences in tqdm(GO_TERM_DICT_80.items()):
        if len(sequences) >= 100:
            training_list_100 = random.sample(sequences, 100)
            training_dict_100[term] = training_list_100
        else:
            # TODO 
            # augmentData()
            training_dict_100[term] = augmentData.augmentData(sequences, 100) 

    for term, sequences in GO_TERM_DICT_20.items():
        if len(sequences) >= 100:
            testing_list_100 = random.sample(sequences, 100)
            testing_dict_100[term] = testing_list_100
        else:
            # TODO 
            # augmentData()
            testing_dict_100[term] = sequences 
            

    print("Done with parseData")
    # return (training_dict_100, GO_TERM_DICT_20)
    return (training_dict_100, testing_dict_100)

'''
Write each go terms seqeunce to a new file in parentDir/DataForHMM
'''
#try:
#    os.mkdir(os.pardir + "/TrainingDataForHMM")
#except: 
#    print("Training folder already made")
#
#try:
#    os.mkdir(os.pardir + "/TestDataForHMM")
#except: 
#    print("Testing folder already made")
#
#for term, sequences in GO_TERM_LISTS_80.items():
#    fileName = term + ".txt"
#    with open(os.pardir + "/TrainingDataForHMM/" + fileName, 'w') as f:
#        f.write(term + " > ")
#        f.write('\n'.join(sequences))
#
#for term, sequences in GO_TERM_LISTS_20.items():
#    fileName = term + ".txt"
#    with open(os.pardir + "/TestDataForHMM/" + fileName, 'w') as f:
#        f.write(term + " > ")
#        f.write('\n'.join(sequences))

#print("Done creating data to feed into HMM")

'''
This method will iterate through each GoTerm and for terms that have greater than 100 sequences
will randomly select 100. For GoTerms with less than 100 sequences this method will use an HMM
to create/predict additional sequences (up to the limit 100)
'''
if __name__ == "__main__":

    parse()
    sys.exit()
