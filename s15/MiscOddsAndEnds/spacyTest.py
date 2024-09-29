# spacyTest.py
#

import pickle
import spacy

nlp = spacy.load("en_core_web_lg")


if __name__ == "__main__":

    b4tagging = pickle.load(open('pickleJar/b4tagging.p', 'rb'))

    for book in b4tagging:
        print(book[0]) # Book name
        for sentence in book[1]: # Has hyphens
            
            print(sentence)

            doc = nlp(' '.join(sentence))

            for token in doc:
                print(token.__len__)

            print('----------')
