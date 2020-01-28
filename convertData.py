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
    
    sequenceData = []
    for sequence in sequences:
        tmpList = []
        for char in sequence:
            tmpList.append(formatMap[char])
        sequenceData.append(tmpList)
        

    return sequenceData

'''
takes a sequence in the form [A,B,C,D,E...,Z] and returns a list in the from [1,2,3,4,5...,26]
'''
def augmentDataToHMMForm(sequence):
    pass
'''
Takes a sequence in the form [1,2,3,4,5,...,26] and returns a list in the form [A,B,C,D,E,...,Z]
'''
def augmentDataFromHMMForm(sequence):
    pass
