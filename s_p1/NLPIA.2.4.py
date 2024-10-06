# NLPIA.2.4.py
# Listing 2.4 from NLPIA, but "Abe the Service Dog"

import pickle
import numpy as np
import pandas as pd

from collections import Counter

pickleInputFile = 'pickleJar/b4tagging.p'


def loadPickleData():

    with open(pickleInputFile, 'rb') as fp:
        corpora = pickle.load(fp)
#        print('Aunt Bee loaded corpora pickle.')
    fp.close()

    return corpora


#
if __name__ == "__main__":

    tokens = []

    corpora = loadPickleData()

    for c in corpora:
        #print("bookName: ", c[0])
        for s in c[1]:
            #print(s)
            tokens = tokens + s

    print('---------')
#    for t in tokens:
#        print(t)

    bow = Counter(tokens)
#
#    print(bow)

    word = 'I'
    times_word_appears = bow[word]
    num_unique_words = len(bow)

    tf = times_word_appears / num_unique_words

    print(round(tf, 4))
    
