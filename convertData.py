import os
import re
from tqdm import tqdm



def convertData(GO_TERM_LISTS_80, GO_TERM_LISTS_20):

    '''
    Write each go terms seqeunce to a new file in parentDir/DataForHMM
    '''
    try:
        os.mkdir(os.pardir + "/TrainingDataForHMM")
    except: 
        print("Training folder already made")

    try:
        os.mkdir(os.pardir + "/TestDataForHMM")
    except: 
        print("Testing folder already made")
    
    print("\nWriting training data to files...")
    for term, sequences in tqdm(GO_TERM_LISTS_80.items()):
        fileName = term + ".txt"
        with open(os.pardir + "/TrainingDataForHMM/" + fileName, 'w') as f:
            sequenceData = formatData(sequences)
            for sequence in sequenceData:
                f.write('-'.join(str(i) for i in sequence))
                f.write('\n')
                
            #f.write(term + " > ")
            #f.write('\n'.join(sequences))
    print("\nWriting Test data to files...")
    for term, sequences in tqdm(GO_TERM_LISTS_20.items()):
        fileName = term + ".txt"
        with open(os.pardir + "/TestDataForHMM/" + fileName, 'w') as f:
            sequenceData = formatData(sequences)
            for sequence in sequenceData:
                f.write('-'.join(str(i) for i in sequence))
                f.write('\n')
            
            #f.write(term + " > ")
            #f.write('\n'.join(sequences))

    print("Done creating data to feed into HMM")

def formatData(sequences):
    formatMap = {

            "A": 1, 
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8,
            "I": 9,
            "J": 10,
            "K": 11,
            "L": 12,
            "M": 13,
            "N": 14,
            "O": 15,
            "P": 16,
            "Q": 17,
            "R": 18,
            "S": 19,
            "T": 20,
            "U": 21,
            "V": 22,
            "W": 23,
            "X": 24,
            "Y": 25,
            "Z": 26,
            " ": 27
            }

    sequenceData = []
    for sequence in sequences:
        tmpList = []
        for char in sequence:
            tmpList.append(formatMap[char])
        sequenceData.append(tmpList)
        

    return sequenceData


