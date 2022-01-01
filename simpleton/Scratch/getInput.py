#
# getInput.py
# Get imput from user
#

import nltk
from nltk import word_tokenize


def getSentence():

    s = input("Enter a short sentence: ")

    tok_s = word_tokenize(s)

    print("You entered the" , len(tok_s), "words:" , tok_s)

    print('Original s: ' + str(s))


    return (s, tok_s)

