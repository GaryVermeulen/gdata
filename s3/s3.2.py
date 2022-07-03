#
# Simpleton data testing
#

from datetime import datetime

fCFG = 'simp.cfg'
fData = 'data.txt'
fHistory = 'history.txt'


def getAllData():

    allData = []
    
    with open(fData, 'r') as f:       
        while (line := f.readline().rstrip()):
            if '#' not in line:
                line = line.replace(' ', '')
                line = line.split(";")

                if line[0] != '#':
                #    print(line)
                    allData.append(line)
                
    f.close()
    return allData

# END getAllData()

# What kind of knowledge can we glean?
#

#rawSentence = ['Mary', 'walked', 'Pookie', 'in', 'the', 'park']

rawSentence = ['Mary', 'saw', 'Pookie', 'with', 'a', 'telescope']

#rawSentence = ['Mary', 'eats', 'telescopes', 'in', 'the', 'park']

#rawSentence = ['ducks', 'flies', 'bus', 'in', 'the', 'telescope']

#rawSentence = ['Pookie', 'ate', 'the', 'bus']

#rawSentence = ['Pookie', 'ate', 'in', 'the', 'bus']

#rawSentence = ['John']

rawSentenceLen = len(rawSentence)


print('Raw sentence: ' + str(rawSentence))
print(rawSentenceLen)

# TO DO:
# Pass rawSentence to Earley Paser which will return:
#   1: Sentence is or is not grammariclly correct
#   2: POS Tags

#epSentence = [('Mary', 'NNP'), ('walked', 'VBD'), ('Pookie', 'NNP'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN')]

epSentence = [('Mary', 'NNP'), ('saw', 'VBD'), ('Pookie', 'NNP'), ('with', 'IN'), ('a', 'DT') , ('telescope', 'NN')]

#epSentence = [('Mary', 'NNP'), ('eats', 'VBZ'), ('telescopes', 'NNS'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN')]

#epSentence = [('ducks', 'NNS'), ('flies', 'VBZ'), ('bus', 'NN'), ('in', 'IN'), ('the', 'DT'), ('telescope', 'NN')]

#epSentence = [('Pookie', 'NNP'), ('ate', 'VBD'), ('the', 'DT'), ('bus', 'NN')]

#epSentence = [('Pookie', 'NNP'), ('ate', 'VBD'), ('in', 'IN'), ('the', 'DT'), ('bus', 'NN')]

#epSentence = [('John', 'NNP')]


print('Parsed sentence: ' + str(epSentence))


print('-----------')

sentenceData = []
bigData = getAllData()

for line in bigData:

    res = any(item in rawSentence for item in line)

    if res:
        sentenceData.append(line)

    
for line in sentenceData:
    print(line)

dataSentence = []

for word in rawSentence:
    for wordData in sentenceData:
        if word == wordData[0]:
            dataSentence.append(tuple((word, wordData)))

print('--------')
for word in dataSentence:
    print(word)

print('----x----')

parsedDataSentence = []

for word in epSentence: 
    for wordData in sentenceData:
        if word[0] == wordData[0]:
            if word[1] == wordData[1]:
                parsedDataSentence.append(tuple((word, wordData)))

for word in parsedDataSentence:
    print('pds-word ' + str(word))

print('--------')

# wh-determiner simplistic solution
# Can we determine:
# who, when, where, what, which, how, why
#

# WHO
# For now just using simple NP VP to determine subject and object
whoLst = []
whoFound = False # Trips on the first noun found to be the subject
print('WHO:')
for who in parsedDataSentence:
    if ('NNP' in who[1]) and not whoFound:
        print('\t Subject: ' + str(who[1][0]))
        whoLst.append(who[1][0])
        whoLst.append('Subject')
        whoFound = True
    elif ('NNP' in who[1]) and whoFound:
        print('\t Object: ' + str(who[1][0]))
        whoLst.append(who[1][0])
        whoLst.append('Object')
    elif ('NN' in who[1]) and whoFound:
        print('\t Object: ' + str(who[1][0]))
        whoLst.append(who[1][0])
        whoLst.append('Object')
    

# WHEN
# Assumptions:
#   VB  - Implies now
#   VBD - Implies past tense
#   VBG - Implies now
#   VBN - Implies past tense
#   VBZ - Impiles now
whenLst = []
print('WHEN:')
for when in parsedDataSentence:
    if when[1][1] in 'VB, VBG, VBZ':
        #print(when[1])
        print('\t' + str(when[1][0]) + ' Implies now')
        whenLst.append(when[1][0])
        whenLst.append('Implied present')
    elif when[1][1] in 'VBD, VBN':
        print('\t' + str(when[1][0]) + ' Implies sometime in the past')
        whenLst.append(when[1][0])
        whenLst.append('Implied past')
    
        
# WHERE
whereLst = []
print('WHERE:')
for where in parsedDataSentence:
    if 'NN' in where[1]:
        if 'p' in where[1][2]:
            #print(where[1][2])
            print('\t' + str(where[1][0]))
            whereLst.append(where[1][0])
# WHAT
print('WHAT:')
# Pronoun:  'What is your name?'
#           'What we need is commitment'
# Determiner:   'What time is it?'
#               'He was robbed of what little money he had'
# Adverb:   'What does it matter?'
#           'What about half?'
# For now we will just show action VBx
whatLst = []
for what in parsedDataSentence:
    if what[1][1] in 'VB, VBD, VBG, VBN, VBZ':
        print('\t' + str(what[1][0]))
        whatLst.append(what[1][0])
    
   
# WHICH
whichLst = []
print('WHICH: TODO')
print('\t Which is Which')
whichLst.append('WHICH-TODO')
'''
pronoun · determiner
determiner: which

    asking for information specifying one or more people or things from a definite set.
    "which are the best varieties of grapes for long keeping?"

pronoun · determiner
pronoun: which

    used referring to something previously mentioned when introducing a clause giving further information.
    "a conference in Vienna which ended on Friday"
'''

# HOW
howLst = []
print('HOW:')
'''
adverb: how

    1.
    in what way or manner; by what means.
    "how does it work?"
    2.
    used to ask about the condition or quality of something.
    "how was your vacation?"
    used to ask about someone's physical or mental state.
    "how are the children?"
    3.
    used to ask about the extent or degree of something.
    "how old are you?"
    used to express a strong feeling such as surprise about the extent of something.
    "how kind it was of him"
    4.
    the way in which; that.
    "she told us how she had lived out of a suitcase for a week"
    in any way in which; however.
    "I'll do business how I like"
'''
for how in parsedDataSentence:
    if how[1][1] in 'VB, VBD, VBG, VBN, VBZ':
        print('\t' + str(how[1][0]))
        howLst.append(how[1][0])

# WHY
whyLst = []
print('WHY: TODO')
print('\t This could loop forever...')
whyLst.append('WHY-TODO')





# Save to valid sentence history file
#

# Valid CFG?
vCFG = True

# Get time and format it
now = datetime.now()
#print(now)
nowf = now.strftime("%m/%d/%Y %H:%M:%S:%f")
print(nowf)

print('Saving history...')
f = open(fHistory, 'a')
f.write(str(epSentence) + '; ' + str(vCFG) + '; ' + str(whoLst) + '; ' +\
        str(whenLst) + '; ' + str(whereLst) + '; ' + str(whatLst) + '; ' +\
        str(whichLst) + '; ' + str(howLst) + '; ' + str(whyLst) + '; ' + nowf + '\n')
f.close()
