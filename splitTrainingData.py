import math
import os
import sys
import shutil

def split(args):
    '''
    args[0] = path to training
    args[1] = path to second output
    args[2] = path to third output 

    '''
    print(args)
    try:
        os.mkdir(args[1])
    except:
        print(f"{args[1]} folder already made")
    try:
        os.mkdir(args[2])
    except:
        print(f"{args[2]} folder already made")
    try:
        os.mkdir(args[3])
    except:
        print(f"{args[3]} folder already made")
    try:
        os.mkdir(args[4])
    except:
        print(f"{args[4]} folder already made")

    trainingFilesList = []

    try:
        trainingFiles = os.listdir(args[0])
    except: 
        print(f"{args[0]} not found... exiting")
        sys.exit()

    firstForty = round(len(trainingFiles)*.40)
    secondForty = firstForty + firstForty
    firstTen = secondForty + round(len(trainingFiles)*.10)
    secondTen = firstTen + round(len(trainingFiles)*.10)

    firstSplit = trainingFiles[0:firstForty]
    secondSplit = trainingFiles[firstForty:secondForty]
    thirdSplit = trainingFiles[secondForty:firstTen]
    fourthSplit = trainingFiles[firstTen:]


    for x in firstSplit: 
        if x in secondSplit or x in thirdSplit or x in fourthSplit: 
            print(f"found {x} in other split, {x} in first split")
            sys.exit()
    for x in secondSplit: 
        if x in firstSplit or x in thirdSplit or x in fourthSplit: 
            print(f"found {x} in other split, {x} in second split")
            sys.exit()
    for x in thirdSplit: 
        if x in firstSplit or x in secondSplit or x in fourthSplit: 
            print(f"found {x} in other split, {x} in third split")
            sys.exit()
    for x in fourthSplit: 
        if x in firstSplit or x in secondSplit or x in thirdSplit: 
            print(f"found {x} in other split, {x} in fourthSplit")
            sys.exit()
               
    for fileName in firstSplit: 
        shutil.copy(args[0] + fileName, args[1])
    print(f"copied files to {args[1]}")
    for fileName in secondSplit: 
        shutil.copy(args[0] + fileName, args[2])
    print(f"copied files to {args[2]}")
    for fileName in thirdSplit: 
        shutil.copy(args[0] + fileName, args[3])
    print(f"copied files to {args[3]}")
    for fileName in fourthSplit: 
        shutil.copy(args[0] + fileName ,args[4])
    print(f"copied files to {args[4]}")



if __name__ == "__main__":
    split(sys.argv[1:])
