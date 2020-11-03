import shutil
import sys
import os
from collections import OrderedDict
import re

"""
    This will take in raw data and convert it into an ordered dictionary
    where the Key is the Sequence and the value is the GoTerms
"""

file_path = os.pardir +  "/functionResource/data/New_filtered_balanced_protein_language_data_34567_top2000"

UNIPROT = OrderedDict()

raw_data = open(file_path, 'r').read().strip()
raw_data = re.split('[|]+|\n+', raw_data)


for i in range(0,len(raw_data), 2):
    sequence = raw_data[i].replace(' ', '')
    function = raw_data[i+1].split(" ")

    UNIPROT[sequence] = function


"""
    This will create a dictionary where Key is GoTerm (alphabet) and the 
    Value is all the associated sequences
"""

GOTERMSDICT = {} 

for sequence in list(UNIPROT.keys()): 
    terms = UNIPROT[sequence]
    for term in terms: 
        if GOTERMSDICT.get(term) != None: 
            GOTERMSDICT.get(term).append(str(sequence))

        else: 
            GOTERMSDICT[term] = []
            GOTERMSDICT[term].append(str(sequence))



"""
This will take a dictionary and filter for the specific 3000 GoIDs that
    have more than 100 sequences.
"""

GOTERMSCOUNT = {}

for sequence, terms in UNIPROT.items():
    for term in terms: 
        if GOTERMSCOUNT.get(term) != None:
            GOTERMSCOUNT[term] += 1

        else:
            GOTERMSCOUNT[term] = 1
over100 = []
for term, count in GOTERMSCOUNT.items():
#    print("{}: {} sequences".format(term, count))
    
    if count >= 100:
        over100.append(term + ".txt")


training_files = os.listdir(sys.argv[1])
#os.mkdir(sys.argv[2])
output_path = sys.argv[2]

for file in training_files:
    if file in over100:
        shutil.copyfile(sys.argv[1] + file, output_path + file)
print("files copied sucessfully")