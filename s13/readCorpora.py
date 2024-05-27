#
# readCorpora.py
#
# Read input book(s)...
#
import sys

from collections import Counter

from commonUtils import connectMongo
from findSVO import findSVO



def findPronounReference(svoObj):
    # This verson only checks the svoObj.inputSent for the nearest antecedent.
    # Need to develope a version to check preceding sentences...

    def getAntecedent(pronoun):

        antecedent = ''
        partialSent = []

        print('**** ', svoObj.inputSent)

        for word in svoObj.inputSent:
            partialSent.append(word)
            if word[0] == pronoun[0]:
                break

        print('**** ', partialSent)
        
        proNoun = partialSent[-1]

        print('****proNoun: ', proNoun)
        
        # Search partial sentence backwards for first antecedent.
        for i, e in reversed(list(enumerate(partialSent))): # i = index, e = element
            print('**** i, e: ', i, e)
            if e[1] in ['NNP', 'NN']: # stop and match 1st NNP to proNoun
                print('****e: {} is NNP'.format(e))
                
                # 1) Has this NNP already7 been matched?
                # 2) Is the NNP MALE or FEMALE?
                # For now, just blindly return NNP
                 
                
                if svoObj.isVar('_PRONOUNMATCH'):
                    for matched in svoObj._PRONOUNMATCH:   # 1)
                        print('**** matched: ', matched)
                        if matched[1][0] == e[0]:
                            print('**** MATCHED.')
                            break
                        else:
                            print('**** NO MATCH ADD')
                            proNounMatch = [proNoun, e]
                            svoObj._PRONOUNMATCH.append(proNounMatch)
                        
                else:
                    svoObj._PRONOUNMATCH = []
                    proNounMatch = [proNoun, e]
                    svoObj._PRONOUNMATCH.append(proNounMatch)
                
                
        return antecedent

    

    if svoObj.isVar('_PRPX'):
        for pronoun in svoObj._PRPX:
            
            if pronoun[0] in ['I', 'me', 'Me', 'my', 'My', 'mine', 'Mine', 'myself', 'Myself']:
                proNounRef = ((pronoun, 'FIRST-PERSON'))
                
            elif pronoun[0] in ['you', 'You', 'your', 'Your', 'yours', 'Yours', 'yourself', 'Yourself']:
                proNounRef = ((pronoun, 'SECOND-PERSON'))
                
            elif pronoun[0] in ['he', 'He', 'him', 'Him', 'his', 'His', 'himself', 'Himself']:
                proNounRef = ((pronoun, 'THIRD-PERSON-MALE'))
                
            elif pronoun[0] in ['she', 'She', 'her', 'Her', 'hers', 'Hers', 'herself', 'Herself']:
                proNounRef = ((pronoun, 'THIRD-PERSON-FEMALE'))
                
            elif pronoun[0] in ['it', 'It', 'its', 'Its', 'itself', 'Itself']:
                proNounRef = ((pronoun, 'THIRD-PERSON'))
                
            elif pronoun[0] in ['we', 'We', 'us', 'Us', 'our', 'Our', 'ours', 'Ours', 'ourselves', 'Ourselves']:
                proNounRef = ((pronoun, 'FIRST-PERSON-PLURAL'))
                
            elif pronoun[0] in ['you', 'You', 'your', 'Your', 'yours', 'Yours', 'yourselves', 'Yourselves']:
                proNounRef = ((pronoun, 'SECOND-PERSON-PLURAL'))
                
            elif pronoun[0] in ['they', 'They', 'them', 'Them', 'their', 'Their', 'theirs', 'Theirs', 'themselves', 'Themselves']:
                proNounRef = ((pronoun, 'THIRD-PERSON-PLURAL'))
                
            else:
                proNounRef = ((pronoun, 'UNDETERMINED'))

                
            if svoObj.isVar('_PRONOUNREF'):
                svoObj._PRONOUNREF.append(proNounRef)
            else:
                svoObj._PRONOUNREF = []
                svoObj._PRONOUNREF.append(proNounRef)
    else:
        print('_PRPX variable not found--no pronouns.') 

    return svoObj


def matchPronouns(svoObj):

    # Checking one sentence i.e. svoObj

    pronounMatches = []

    print('matchPronouns input sentence:')
    print(svoObj.inputSent)

    if svoObj.isVar('_PRONOUNREF'):
        for pronoun in svoObj._PRONOUNREF:
            if pronoun[1] == 'THIRD-PERSON-MALE':
                print('### Found THIRD-PERSON-MALE to match: ', pronoun)
                print('pronounMatches":')
                print(pronounMatches)
                # Has this pronoun already been matched?
                for m in pronounMatches:
                    print('m[0]: ', m[0])
                    
                    if m[0] == pronoun:
                        print('already matched')
                        continue
                    else:
                        print('not already matched')

                # Read sentence up to pronoun
                partialSent = []
                for word in svoObj.inputSent:
                    partialSent.append(word)
                    if word[0] == pronoun[0][0]:
                        break

                print('### partialSent: ', partialSent)

                # Search partial sentence backwards for first antecedent.
                rChunk = []
                for i, e in reversed(list(enumerate(partialSent))): # i = index, e = element
                    print('**** i, e: ', i, e)
                    rChunk.append(e)
                    if e[1] in ['NNP']: # stop and match 1st NNP to proNoun
                        print('**** e: {} is NNP'.format(e))
                        chunk = []
                        for c in reversed(rChunk):
                            chunk.append(c)
                        print('** chunk: ', chunk) # Unreverse

                        pronounMatch = [pronoun, e, chunk]

                        print('* pronounMatch: ', pronounMatch)
                        pronounMatches.append(pronounMatch)
                        print('p...Matches: ', pronounMatches)
                        break
                    
                    # 1) Has this NNP already7 been matched?
                    # 2) Is the NNP MALE or FEMALE?
                    # For now, just blindly return NNP




    return svoObj


#
#
#
if __name__ == "__main__":
    
    bookSentenceSubjects = []
    bookSentenceObjects = []

    mdb = connectMongo()
    simpDB = mdb["simp"]
    taggedCorpora = simpDB["taggedCorpora"]

    cursorLst = list(taggedCorpora.find({}))

    for c in cursorLst:
        print(c["bookName"])
        print('======')
        for s in c["taggedSentences"]:
            print('s:')
            print(s)
            print('---')

            # Corrections?
            #  Tagging errors: ['Moebus', 'NNP'] and '['Moebus', 'NN'], and ['goldfish', 'JJ']
            #  How to deal with: ['Pop', 'NNP'], ['Pop', 'NNP'] to ['Pop Pop', 'NNP']
            #
            
            print('findSVO...')
            svoObj = findSVO(s) # Creates Sentence object instance svoObj
            print('svoObj:')
            svoObj.printAll()
            print('---')
            
            print('findPronounReference...')
            svoObj = findPronounReference(svoObj)
            print('AFTER findPronounReference svoObj:')
            svoObj.printAll()
            print('---')

            print('matchPronouns...')
            svoObj = matchPronouns(svoObj)
            print('AFTER matchPronouns svoObj:')
            svoObj.printAll()
            print('---')
            

            

            for subj in svoObj.subject:
                bookSentenceSubjects.append(subj)

            for obj in svoObj.object:
                bookSentenceObjects.append(obj)
            

        print('------')

        print('bookSentenceSubjects:')
        print(bookSentenceSubjects)

        print('------')

        subjects = []
        for item in bookSentenceSubjects:
            subjects.append(item[0]) 

        x = Counter(subjects)

        print(x)

        print('------')

        print('bookSentenceObjects:')
        print(bookSentenceObjects)

        print('------')

        objects = []
        for item in bookSentenceObjects:
            objects.append(item[0]) 

        x = Counter(objects)

        print(x)
        
