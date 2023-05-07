#
# tagTest.py
#

import spacy




if __name__ == "__main__":


#    testSentence = 'what do you do in the morning'
#    testSentence = 'i do not know what a cow does'
#    testSentence = 'if you are only using the month and year you do not use a comma'
#    testSentence = 'dry kibble is clearly not enough to sustain a voracious dog like Sally'
#    testSentence = 'i do not fell well today'
    testSentence = 'I am hungry because I did not eat lunch.'

    nlp = spacy.load("en_core_web_sm") # Going for the best accuracy

    doc = nlp(testSentence)

    tmpDoc = []
    for token in doc:            
        tmpToken = ((str(token.text)), (str(token.tag_)))
        tmpDoc.append(tmpToken)

#    taggedDocs.append(tmpDoc)

    print(tmpDoc)
