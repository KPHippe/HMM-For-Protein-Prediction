import os
import re

"""
 This will open a .fasta file and turn it into a dictionary.
 The key -> is the proteinID number.
 The value -> unique sequence for protID
"""
def readFasta(f):

    name, sequence = None, []
    for line in f:
        line = line.rstrip()
        if line.startswith('>'):
            if name: yield (name, ''.join(sequence))
            name, sequence, = line, []
        else:
            sequence.append(line)
    if name: yield (name, ''.join(sequence))


    #with open(pathToFile , 'r') as f:
    #    f = f.read().strip()
    #    f = f.split(">")

    #    res_dct = {f[i]: f[i + 1] for i in range(0, len(f), 2)}
    #    #print("{" + "\n".join("{!r}: {!r}".format(k, v) for k, v in res_dct.items()) + "}")


    #return res_dct

"""
 This will open all three leafonly files, convert them to one long string.
 Then create a dictionary where key -> proteinID number.
 The value -> GoID *MAY HAVE MULTIPLE GO TERMS TO SAME PROTEINID*
 When this happens a list is created and appeneded with the values (GoIDs) 
"""
def getSelectedGroundTruths(pathToFile):


    with open(pathToFile + 'leafonly_BPO_unique.txt', 'r') as a, open(pathToFile + 'leafonly_CCO_unique.txt', 'r') as b, open(pathToFile + 'leafonly_MFO_unique.txt', 'r') as c:
        all_inputs_as_1string = a.readlines() + b.readlines() + c.readlines()
        list_of_all_protID_and_goTerm = []
        dict_of_protID_and_goTerm = {}
        for line in all_inputs_as_1string:
            line = re.split("[\t]+|[\n]+", line)
            del line[2]
            list_of_all_protID_and_goTerm.append([line[0], line[1]])


        for line in list_of_all_protID_and_goTerm:

            if line[0] not in dict_of_protID_and_goTerm.keys():

                dict_of_protID_and_goTerm[line[0]] = [line[1]]
            else:

                dict_of_protID_and_goTerm[line[0]].append(line[1])
        


        return dict_of_protID_and_goTerm
    
"""
    Ths will convert F_3_GO_table.DAT files to dictionary where
    key - > GoID and
    value -> GoTerms (alphabetic representation, no numbers/integers)
"""

def establishGOIDtoTermRelations(pathToFile):


    goID_to_term_dict = {}
    goTerm_to_ID_dict = {}
    with open(pathToFile + 'F_3_GO_table.DAT', 'r') as f:
        f = f.read().strip()
        f = re.split('[\s]+', f)

        goID_to_term_dict = {f[i]: f[i + 1] for i in range(0, len(f), 2)}
        goTerm_to_ID_dict = {f[i+1]: f[i] for i in range(0, len(f), 2)}

        #need to have these structures persist onece this mehtod is called
        #return ID to Term first index, Term to ID second index
        return (goID_to_term_dict, goTerm_to_ID_dict)
