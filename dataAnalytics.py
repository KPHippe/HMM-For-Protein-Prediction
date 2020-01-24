import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt

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

totalGOTerms = 0
goTermMaxLength = 0
for key, value in UNIPROT.items():
    goLength = len(value)
    if goLength > goTermMaxLength:
        goTermMaxLength = goLength

    totalGOTerms += 1


print("Average number of GO terms per sequnce: {}".format(totalGOTerms//len(UNIPROT)))
print("Maximum lenght of GO terms for singal sequence: {}".format(goTermMaxLength))

'''

More analytics here
Finding the number of sequences that fall in each category to get accurate read on how much data we
have


'''

GOTERMSCOUNT = OrderedDict()

maxSequencePerGOTerm = (0, None)
totalSequeneNum = 0
for sequence, terms in UNIPROT.items():
    for term in terms: 
        if GOTERMSCOUNT.get(term) != None:
            GOTERMSCOUNT[term] += 1

        else:
            GOTERMSCOUNT[term] = 1

for term, count in GOTERMSCOUNT.items():
#    print("{}: {} sequences".format(term, count))
    totalSequeneNum += GOTERMSCOUNT[term]
    if count > maxSequencePerGOTerm[0]:
        maxSequencePerGOTerm = (count, term)

print("Total different go terms in this database: {}".format(len(GOTERMSCOUNT)))
print("Average number of sequences per go term: {}".format(totalSequeneNum//len(GOTERMSCOUNT)))
print("Max number of seqeunces for a go term: {} ({})".format(maxSequencePerGOTerm[0], maxSequencePerGOTerm[1]))


'''

plotting stuff here

x axis -> categories (eg 1 occurence, 2 occurence)
y axis -> density

'''

termsCountList = []

for term, count in GOTERMSCOUNT.items():
    termsCountList.append(count)

#print(*termsCountList)
plotData = []
termsCountList = sorted(termsCountList)


numBins = 180

fig, ax = plt.subplots()

n, bins, patches = ax.hist(termsCountList,numBins, density=1)

ax.set_xlabel("Number of occurences of seqeuneces that match to go term")
ax.set_ylabel("Density")

plt.show()




