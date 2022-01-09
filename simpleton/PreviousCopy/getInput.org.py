#
# Get imput from user
#

import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn

def getSentence():

    s = input("Enter a short sentence: ")

    tok_s = word_tokenize(s)

    print("You entered the" , len(tok_s), "words:" , tok_s)

    pos_s = nltk.pos_tag(tok_s)
    print('POS: ' + str(pos_s))

    print('Original s: ' + str(s))


    return s
