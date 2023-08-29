#
# inflectionTest.py
#

import spacy
import pyinflect

from commonUtils import connectMongo


def buildInflections():

    verbs = ''
    verbsList = []
    verbsNotFound = []
    nlp = spacy.load("en_core_web_lg")
    mdb = connectMongo()
    simpDB = mdb["simp"]
    taggedBoW = simpDB["taggedBoW"]
    verbInflections = simpDB["verbInflections"]
    

    taggedBoWList = list(taggedBoW.find())

    for taggedWord in taggedBoWList:
        if taggedWord["tag"] in ['VB', 'VBG', 'VBD', 'VBN']:
            if len(verbs) == 0:
                verbs = taggedWord["word"]
            else:
                verbs = verbs + ' ' + taggedWord["word"]
    

    #verbs = "eating goes touch felt hit sleeping"
    doc = nlp(verbs)
    cnt = 1
    for token in doc:
        base = token._.inflect("VB")
        gerund = token._.inflect("VBG")
        past_tense = token._.inflect("VBD")
        past_participle = token._.inflect("VBN")
        print(token.text, "-", base, "-", gerund, "-", past_tense, "-", past_participle)

        if base == None or gerund == None or past_tense == None or past_participle == None:
            verbsNotFound.append({"_id": token.text, "base": base, "gerund": gerund, "past_tense": past_tense, "past_participle": past_participle})
        else:
            if token.text in verbsList:
                tokenText = token.text + "_" + str(cnt)
                verbInflections.insert_one({"_id": tokenText, "base": base, "gerund": gerund, "past_tense": past_tense, "past_participle": past_participle})
                verbsList.append(tokenText)
            else:
                verbInflections.insert_one({"_id": token.text, "base": base, "gerund": gerund, "past_tense": past_tense, "past_participle": past_participle})
                verbsList.append(token.text)
        cnt =+ 1

    return verbsNotFound


if __name__ == "__main__":

    verbsNotFound = buildInflections()

    print("verbsNotFound:")
    for i in verbsNotFound:
        print('- ', i)
