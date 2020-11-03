import os
import sys
import math
import copy
import time
import random
import numpy as np
from hmmlearn import hmm

import Augment.convertData
import Augment.convertData

'''
augmentData takes a list of 1 or more seqeunces and uses an HMM to augment the data into a list of n
sequences to unbias the training

Arguements: seqeunces -> list of one or more seqeunces
            n -> the size of the new list to be returned

returns: newData -> list of size n the follows the format of data to be fed to HMM
'''
def augmentData(term, sequences, n, path_to_output):
    newSequences = []

    avgLengthOfSequences = 0
    for sequence in sequences:
        avgLengthOfSequences += len(sequence)

    avgLengthOfSequences = avgLengthOfSequences//len(sequences)


    '''convertData to HMM seqeunce'''
    convertedSequences = convertData.augmentDataToHMMForm(sequences)
    #Add these converted seqeucnes to the newSequences list to get everythin in the right form

    for seq in convertedSequences:
        newSequences.append(seq)

    '''Build hmm'''

    model = hmm.GaussianHMM(n_components=5, covariance_type='full', n_iter=1000)

    dataForHMM = np.array([])
    lengths = []
    for sequence in convertedSequences:
        dataForHMM = np.append(dataForHMM, sequence)
        lengths.append(len(sequence))

    dataForHMM = dataForHMM.astype(np.float64)
    dataForHMM = np.reshape(dataForHMM, (-1, 1))

    model.fit(dataForHMM, lengths)

    '''Sample HMM to build 'deep faked' data '''

    for _ in range(len(sequences), n, 1):
        #sample the data from the model
        nLengthSequence = random.randint(round(avgLengthOfSequences*.90), round(avgLengthOfSequences*1.10))
        newData = model.sample(nLengthSequence)[0]
        convertedData = convertData.formatOutputFromHMM(newData)

        #add the seqeunce to the new data
        newSequences.append(convertedData)


    '''convert this list of seqeucnes'''
    newSequences = convertData.augmentDataFromHMMForm(newSequences)
    writeToFile(term, newSequences, path_to_output)


def writeToFile(term, sequences, path_to_output):

    try:
        os.mkdir(path_to_output)
        print(f"{path_to_output} made...")
    except:
        pass

    formattedSequences = convertData.formatData(sequences)

    fileName = term + ".txt"
    with open(path_to_output + fileName, 'w') as f:
            for sequence in formattedSequences:
                f.write('-'.join(str(i) for i in sequence))
                f.write('\n')

    print(f"{term} written to file")
