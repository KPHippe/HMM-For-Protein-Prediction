import parseData
import convertData

import sys
import os
import time
import re
from collections import OrderedDict
import numpy as np
import random
from tqdm import tqdm


def main():
    GO_TERM_LISTS = parseData.parse()

    GO_TERM_LISTS_80 = GO_TERM_LISTS[0]

    GO_TERM_LISTS_20 = GO_TERM_LISTS[1]

    '''

    create all the files

    '''
    convertData.convertData(GO_TERM_LISTS_80, GO_TERM_LISTS_20)
    sys.exit()
    '''
    
    file that trains everything here

    '''

    '''
    
    something that predicts here

    '''


if __name__ == '__main__':
    main()
