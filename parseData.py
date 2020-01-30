import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import random

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
    GOTERMSLISTS = {} 

    for sequence in list(UNIPROT.keys()): 
        terms = UNIPROT[sequence]
        for term in terms: 
            if GOTERMSLISTS.get(term) != None: 
                GOTERMSLISTS.get(term).append(str(sequence))

            else: 
                GOTERMSLISTS[term] = []
                GOTERMSLISTS[term].append(str(sequence))
    bannedTerms = set()
    bannedTerms.add("PRN")
    bannedTerms.add("CON")

    for term, sequences in GOTERMSLISTS.items():
        if len(sequences) > 10000:
            bannedTerms.add(term)

    GO_TERM_LISTS_80 = OrderedDict()
    GO_TERM_LISTS_20 = OrderedDict()

    for sequence in eightyPercent: 
        terms = UNIPROT[sequence]
        for term in terms:
            if term not in bannedTerms:

                if GO_TERM_LISTS_80.get(term) != None: 
                    GO_TERM_LISTS_80.get(term).append(str(sequence))

                else: 
                    GO_TERM_LISTS_80[term] = []
                    GO_TERM_LISTS_80[term].append(str(sequence))
           
           
    for sequence in twentyPercent: 
        terms = UNIPROT[sequence]
        for term in terms:
            if term not in bannedTerms:

                if GO_TERM_LISTS_20.get(term) != None: 
                    GO_TERM_LISTS_20.get(term).append(str(sequence))

                else: 
                    GO_TERM_LISTS_20[term] = []
                    GO_TERM_LISTS_20[term].append(str(sequence))
        

    flag = False
    for term, seqeunces in GO_TERM_LISTS_80.items():
        if len(seqeunces) > 10000:
            flag = True

    if flag: 
        print("Saw something over 10k in training set")
    else: 
        print("cleaning successful")


    flag = False
    for term, seqeunces in GO_TERM_LISTS_20.items():
        if len(seqeunces) > 10000:
            flag = True

    if flag: 
        print("Saw something over 10k in test set")
    else: 
        print("cleaning successful")



    return (GO_TERM_LISTS_80, GO_TERM_LISTS_20)

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

