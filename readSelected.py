import os
import re


with open('selected.fasta', 'r') as f:
    f = f.read().strip()
    f = f.split("\n")

    res_dct = {f[i]: f[i + 1] for i in range(0, len(f), 2)}
    #print("{" + "\n".join("{!r}: {!r}".format(k, v) for k, v in res_dct.items()) + "}")
    
with open('leafonly_BPO_unique.txt', 'r') as a, open('leafonly_CCO_unique.txt', 'r') as b, open('leafonly_MFO_unique.txt', 'r') as c:
    all_inputs_as_1string = a.readlines() + b.readlines() + c.readlines()
    list_of_all_protID_and_goTerm = []
    dict_of_protID_and_goTerm = {}
    for line in all_inputs_as_1string:
        line = re.split("[\t]+|[\n]+", line)
        del line[2]
        list_of_all_protID_and_goTerm.append([line[0], line[1]])
    #print(list_temp)

    for line in list_of_all_protID_and_goTerm:
        #print(line, line[1])
        if line[0] not in dict_of_protID_and_goTerm.keys():
            #print("inside if")
            dict_of_protID_and_goTerm[line[0]] = [line[1]]
        else:
            #print("inside else")
            dict_of_protID_and_goTerm[line[0]].append(line[1])
    
    for k, v in dict_of_protID_and_goTerm.items():
        print(k, v)

