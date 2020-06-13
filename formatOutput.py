import os
import sys

def format(pathToGOPredictionFile, threshhold):
    with open(pathToGOPredictionFile, 'r') as f:
        text = f.read()

    text = text.split("\n")
    newText = []
    for line in text:
        if "GO:" in line:
            elements = line.split("\t")
            if float(elements[2]) > 0.80:
                newText.append("\t".join(e for e in elements))

        else:
            newText.append(line)

    newText = "\n".join(line for line in newText)

    newFileName = "/".join(e for e in pathToGOPredictionFile.split("/")[:-1]) + "/" +pathToGOPredictionFile.split("/")[-1].split('.')[0] + f"_{threshhold}.txt"
    print(f"Saving to {newFileName}")
    with open(newFileName, 'w') as f:
        f.write(newText)

if __name__ =="__main__":
    pathToGOPredictionFile = sys.argv[1]
    threshhold = 0.80
    if len(sys.argv) > 2:
        threshhold = sys.argv[2]
    format(pathToGOPredictionFile, threshhold)