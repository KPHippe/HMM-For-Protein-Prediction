import os
import sys
from hmmlearn import hmm 
import numpy as np
import math
import convertData
import copy
import random
import time

'''
augmentData takes a list of 1 or more seqeunces and uses an HMM to augment the data into a list of n
sequences to unbias the training

Arguements: seqeunces -> list of one or more seqeunces
            n -> the size of the new list to be returned

returns: newData -> list of size n the follows the format of data to be fed to HMM
'''
def augmentData(sequences, n):
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
    #print("Returning NewSequences in augmentData.py")
    return newSequences

    


if __name__ == '__main__':
    #baxs is a small file, one sequence long
    fileToGrab = "BAXS.txt"
    

    try: 
        baxs = open(os.pardir + "/TrainingDataForHMM/" + fileToGrab, 'r').read().split('-')
        cuhn = open(os.pardir + "/TrainingDataForHMM/" + "CUHN.txt", 'r').read().split()

    except: 
        print(f"An error occured grabbing {fileToGrab}")
        sys.exit()
    print(cuhn)
    sepcuhn = []
    for seq in cuhn:
        seq = seq.split("-")
        sepcuhn.append(int(i) for i in seq)
    baxs = [int(i) for i in baxs]
    letterbaxs = convertData.augmentDataFromHMMForm([baxs])
    lettercuhn = convertData.augmentDataFromHMMForm(sepcuhn) 
     
    #actually do the augmenting here
    augmentedSequences = []
    augmentedSequences = augmentData(letterbaxs, 10)
    augmentedSequences = augmentData(lettercuhn, 100)
    for seq in lettercuhn: 
        print(" ".join(i for i in seq))
    print("This is the result of augmentData:")
    for res in augmentedSequences:
        print(" ".join(i for i in res))


    
