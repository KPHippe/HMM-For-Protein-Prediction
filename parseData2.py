import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
formatMap = {

        "A": [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "B": [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "C": [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "D": [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "E": [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "F": [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "G": [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "H": [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "I": [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "J": [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "K": [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "L": [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "M": [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "N": [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "O": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
        "P": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        "Q": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
        "R": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        "S": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
        "T": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        "U": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        "V": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        "W": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
        "X": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        "Y": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
        "Z": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        " ": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]

        }


DEBUG = False

file_path = os.curdir +  "/functionResource/data/New_filtered_balanced_protein_language_data_34567_top2000"

if len(sys.argv) > 1:
    file_path = os.curdir + sys.argv[1]
'''
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

list_dict_keys = list(UNIPROT.keys())
#eightyPercent = random.sample(dict_keys, round(len(dict_keys)*.8)
random.shuffle(list_dict_keys)
eightyPercent = list_dict_keys[:round(len(list_dict_keys)*.8)]
twentyPercent = list_dict_keys[len(eightyPercent):]
# print("len of whole list is: {}".format())
# print("len of whole is: {}".format(len(list_dict_keys)))
# print("len of 80 is : {}".format(len(eightyPercent)))
# print("len of twentyPercent is: {}".format(len(twentyPercent)))
# file = open("eightyPercent.txt", "w")
# file.write()
with open('trainingEighty.txt', 'w') as file:
    file.write(str(eightyPercent))

with open('trainingTwenty.txt', 'w') as file:
    file.write(str(twentyPercent))

GOTERMSLISTS = OrderedDict()

'''
This function makes a dictionary: 
    key -> GO Term
    value -> list of sequences, no spaces currently
'''
for sequence, terms in UNIPROT.items():
    for term in terms: 
        if GOTERMSLISTS.get(term) != None: 
            GOTERMSLISTS.get(term).append(str(sequence))

        else: 
            GOTERMSLISTS[term] = []
            GOTERMSLISTS[term].append(str(sequence))

# f= open("TEST2.txt", 'w')
# test_string = GOTERMSLISTS.pop('BMCY')
# f.write(str(test_string))
# f.close()

list_data = []
test_string = GOTERMSLISTS.pop('BMCY')
for indx in test_string:
        for char in indx:
            list_data.append(formatMap[char])

# print(list_data)
#for goTERM, sequences in GOTERMSLISTS.items():
#    print("GO TERM: {}, seqeunces: {}".format(goTERM, sequences))
#    time.sleep(5)


