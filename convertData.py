import os
from tqdm import tqdm

formatMap_LetToNum = {

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

formatMap_NumToLet = {

             1 : "A",
             2 : "B",
             3 : "C",
             4 : "D",
             5 : "E",
             6 : "F",
             7 : "G",
             8 : "H",
             9 : "I",
             10 : "J",
             11 : "K",
             12 : "L",
             13 : "M",
             14 : "N",
             15 : "O",
             16 : "P",
             17 : "Q",
             18 : "R",
             19 : "S",
             20 : "T",
             21 : "U",
             22 : "V",
             23 : "W",
             24 : "X",
             25 : "Y",
             26 : "Z",
             27 : " "        
            }



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
            tmpList.append(formatMap_LetToNum[char])
        sequenceData.append(tmpList)
        

    return sequenceData

'''
takes a sequence in the form [A,B,C,D,E...,Z] and returns a list in the from [1,2,3,4,5...,26]
'''
def augmentDataToHMMForm(sequence):
    numSeq = []
    for i in sequence:
        #slowly builds the numSeqence,one num at a time as it corresponds to letter
        numSeq.append(formatMap_LetToNum[i])
        
    return numSeq 

'''
Takes a sequence in the form [1,2,3,4,5...,26] and returns the list in the form [A,B,C,D,E,...,Z]
'''
def augmentDataFromHMMForm(sequence):
    letSeq = []
    for i in sequence:
        #slowly builds the numSeqence,one letter at a time as it corresponds to num
        letSeq.append(formatMap_NumToLet[i])
        
    return letSeq
