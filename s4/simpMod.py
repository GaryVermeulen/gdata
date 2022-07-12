#
# simpMod.py
#
import nltk
from nltk import word_tokenize
#from nltk.corpus import wordnet as wn
from nltk import pos_tag
#import re
import random as rd
import spacy
import pyinflect


# CFG file
#
fCFG = 'simp.cfg'

# Data (kind of a lex and KB)
#
fdata = 'data.txt'

# Log file
#
flog = 'simpLog.txt'

###
def getData():

    inData = []

    with open(fCFG, 'r') as fin:
        
        while (line := fin.readline().rstrip()):
           if '#' not in line:
                line = line.replace(' ', '')
                line = line.split(";")

                if line[0] != '#':
                #    print(line)
                    inData.append(line)

    fin.close()

    return(inData)



###
def getInput():

    s = input("Enter a command <[C]hat, [S]peak, or [T]each>: ")

    if s == 'c' or s == 'C':

        print("Entering Chat mode...")
    elif s == 's' or s == 'S':
        print(s)
        print("Entering random Speak mode...")
    elif s == 't' or s == 'T':
        print(s)
        print("Entering Teach mode...")
    else:
        print("Invalid entry!?" + str(s))

    return s
# end getSentence()

###
def chkGrammar(s):

    simpleGrammar = nltk.data.load('file:' + str(fCFG))

    rd_parser = nltk.RecursiveDescentParser(simpleGrammar) #, trace=2)
##    rd_parser = nltk.RecursiveDescentParser(simpleGrammar, trace=2)
    treesFound = []
    strTrees = []

    slist = s 

    fl = open(flog, 'a')

 
    try:
        for tree in rd_parser.parse(slist):
            treesFound.append(tree)
            print('>' + str(tree) + '<')

        if len(treesFound) == 0:
            fl.write('Input: ' + str(s) + ' - did not produce a tree:\n')
#            tok_s = word_tokenize(s)
            pos_s = nltk.pos_tag(s)
            fl.write('Simple tokenizer: ' + str(pos_s) + '\n')
            retCode = 0
        else:
##?            fmem = open(fm, fmMode)
            fl.write('Input: ' + str(s) + ' - produced:\n')
            for t in treesFound:
                fl.write(str(t))
                fl.write('\n')
                strTrees.append(str(t))

            for st in strTrees:
                print(type(st))
                print(st)
#            tok_s = word_tokenize(s)
            pos_s = nltk.pos_tag(s)
            fl.write('Simple tokenizer: ' + str(pos_s) + '\n')
            
#            retCode = len(treesFound)
            retCode = treesFound
    
    except ValueError as err:
#        print('Problem with input not covered by grammar')
#        print('ValueError: {0}'.format(err))
#        myErrHandler(err)        
#        retCode = -1
        retCode = err
        
    fl.close()
    
    return retCode

# end chkGrammar(s)


###
def myErrHandler(err):

    learningMode = False
    
    print('ErrH: Problem with input not covered by grammar')
    print('ErrH: ValueError: {0}'.format(err))

#    missingWord = re.search('\'(.*)\'', str(err))
#    mw = missingWord.group(1)
#    print(mw)
#
    response = input('Shall we enter learning mode? <Y/N>')

    if (response == 'Y') or (response == 'y'):
        learningMode = True
    
    return learningMode

# end myErrHandler(err):


###
def getNodes(parent):

    ROOT = 'ROOT'
    tree = ...
    
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == ROOT:
                print("======== Sentence =========")
                print("Sentence:", " ".join(node.leaves()))
            else:
                print("Label:", node.label())
                print("Leaves:", node.leaves())

            getNodes(node)
        else:
            print("Word:", node)

# end getNodes(parent)


###
def getJustNouns(pos_s):

    jNouns = []
    
    for i in range(len(pos_s)):
        if pos_s[i] in "NN NNS":
            jNouns.append(pos_s[i - 1])        

    return jNouns
# end getJustNouns


###
def searchMeaning(s, pos_s, names, nouns):

    relationFound = False
    sNames = []
    sNouns = []
    matchedIsA = []
    matchedCanDo = []
    pos_w = ''
    pos_w_tag = ''

    fl = open(flog, 'a')

    print('\tTop of searchMeaning:')
    fl.write('\tTop of searchMeaning: Input:' + str(s) + '\n')

    # Build lists of names and nouns from input sentense

    # return just NNP and NN from pos_s
    jNouns = getJustNouns(pos_s)

    
    for w in s:

        for n in names:
            if w == n.name:
                sNames.append(n)

        if w in jNouns:
       
            for noun in nouns:
                nounInflections = getInflections(noun.name, "NN")
            
                if w in nounInflections:
                    sNouns.append(noun)

    print("\tNNPs Found (" + str(len(sNames)) + ").")
    fl.write("\tNNPs Found (" + str(len(sNames)) + ").\n")
    
    print(str(sNames))
    fl.write(str(sNames) + '\n')
    
    print("\tNNs Found (" + str(len(sNouns)) + ").")
    fl.write("\tNNs Found (" + str(len(sNouns)) + ").\n")
    
    print(str(sNouns))
    fl.write(str(sNouns) + '\n')
    
    print("\t-NNP---------------------")
    fl.write("\t-NNP---------------------\n")
    
    # Of the names found in the input sentense
    # extract their isA(s) and canDo(s)
    for sn in sNames:
#        print("\tNNP Object:")
#        print(sn.name, sn.gender, sn.isA, sn.canDo, sep=' ; ')
        fl.write("\tNNP Object:\n")
        fl.write(sn.name + ' ; ' + sn.gender + ' ; ' + sn.isA + ' ; ' + sn.canDo + '\n')
        isAs = sn.isA
        canDos = sn.canDo
        print("canDos: " + str(canDos))
        fl.write("\tcanDos: " + str(canDos) + "\n")

#        print("\tNNP Obj name: " + str(sn.name))
        fl.write("\tNNP Obj name: " + str(sn.name) + "\n")
        
        if isAs != "UNK":
            isAs = isAs.split(',')
#            print("\tSplit isAs: ")
#            print(str(isAs))
            fl.write("\tSplit isAs: " + str(isAs) + "\n")
        else:
#            print("\tObj isA: ")
#            print(str(sn.isA))
            fl.write("\tObj isA: " + str(sn.isA) + "\n")

        if canDos != "UNK":
            canDos = canDos.split(',')
#            print("\tSplit canDos: ")
#            print(str(canDos))
            fl.write("\tSplit canDos: " + str(canDos) + "\n")

            for w in s:
                # Is w an inflction of one of the canDos?
                # First get possible inflections
                inflecs = getInflections(w, "VB")

 #               print(type(inflecs))
 #               print(inflecs)

                # Now compare
                if w in inflecs:
                    # Ensure w is base verb and not an inflection
                    listInflecs = inflecs.split(",")
                    w = listInflecs[0]
                    
                if w in canDos:
                    print("\tMatch: " + str(sn.name) + " " + str(w))
                    fl.write("\tMatch: " + str(sn.name) + " " + str(w) + "\n")
                    matchedCanDo.append(str(sn.name) + " " + str(w))
                    
        else:
            print("\tObj canDos: " + str(sn.canDo))
            fl.write("\tObj canDos: " + str(sn.canDo) + "\n")
        

    print("\t-NN---------------------")
    fl.write("\t-NN---------------------\n")
    # Of the nouns found in the input sentense
    # extract their isA(s)

    print(sNouns)
    
    for n in sNouns:
        
#        print("\tNN Object:")
#        print(n.name, n.isA, n.canDo, sep=' ; ')
        fl.write("\tNN Object:\n")
        fl.write(n.name + ' ; ' +  n.isA + ' ; ' + n.canDo + '\n')
        isAs = n.isA
        canDos = n.canDo
        
#        print("\tNN Obj name: " + str(n.name))
        fl.write("\tNN Obj name: " + str(n.name))
        
        if isAs != "UNK":
            isAs = isAs.split(',')
#            print("\tSplit isAs: ")
#            print(str(isAs))
            fl.write("\tSplit isAs:\n")
            fl.write(str(isAs) + '\n')
        else:
#            print("\tObj isA: ")
#            print(str(n.isA))
            fl.write("\tObj isA:\n")
            fl.write(str(n.isA) + '\n')
        
        if canDos != "UNK":
            canDos = canDos.split(',')
#            print("\tSplit canDos: ")
#            print(str(canDos))
            fl.write("\tSplit canDos:\n")
            fl.write(str(canDos) + '\n')

            for w in s:

                inflecs = getInflections(w, "VB")

                # Now compare
                if w in inflecs:
                    # Ensure w is base verb and not an inflection
                    listInflecs = inflecs.split(",")
                    w = listInflecs[0]
                
                if w in canDos:
                    print("\tMatch: " + str(n.name) + " " + str(w))
                    fl.write("\tMatch: " + str(n.name) + " " + str(w) + '\n')
                    matchedCanDo.append(str(n.name) + " " + str(w))
            
        else:
            print("\tObj canDos: " + str(n.canDo))
            fl.write("\tObj canDos: " + str(n.canDo) + '\n')

    print("\t-Conclusion---------------------")
    fl.write("\t-Conclusion---------------------\n")

    if len(matchedCanDo) > 0:
        for d in matchedCanDo:
            print("\tmatchedCanDo: " + str(d))
            fl.write("\tmatchedCanDo: " + str(d) + '\n')
            relationFound = True
    else:
        print("\tNo relationships found.")
        fl.write("\tNo relationships found.\n")
        relationFound = False

    fl.close()
    
    return relationFound
# End searchMeaning(s)


###
def addWord(nw):

    tag_not_found = []
    word_added = []
    lines = []
    idx = 0

    print('Entering addWord...')

    nw = nw.replace(",", '')

    tok_nw = word_tokenize(nw)
    pos_nw = pos_tag(tok_nw)

    print('NLTK tagged input as:')
    for w in pos_nw:
        print(w)
        
        response = input('Is the above tag correct <Yy>?')

        if response not in 'Yy':
            c_tag = input('Enter corrrect tag: ')
            w0 = w[0]
            new_w = (w0, c_tag)
            pos_nw[idx] = new_w
            print('You have entered: ' + str(new_w))

        idx = idx + 1

    # Read existing CFG
    with open(fCFG, 'r') as fin:        
        while (line := fin.readline().rstrip()):        
            lines.append(line)
    fin.close()

    inserted = False
    
    # Search for the end of the given section ex: NN, NNP, DT, etc.
    for new in pos_nw:

        nw = new[0]
        nt = new[1]
    
        lin_no = 0
        match = False
        for l in lines:
            l = l.replace("-", '')
            l = l.replace(" ", '')
            l = l.split(">")

            if l[0] == nt:
                match = True

            if l[0] == '#' and match:
                lines.insert(lin_no, str(nt) + ' -> "' + str(nw) +'"')
                inserted = True
                break

            lin_no += 1
        
    # Overwrite with new input
    f = open(fCFG, 'w')
    for l in lines:
        f.write(l + '\n')
    f.close()

    print('End addWord.')
      
    return

# End addWord()


###
def learningMode(nW):
    #
    # Scaled back to just add words
    #

    nWs = []
    
    print('Learning Mode:')
    print(nW)

    missingWord = re.search('\'(.*)\'', str(nW))    
    nW = missingWord.group(1)
    nW = nW.replace("'", '')

    addWord(nW)
    

    print('Exiting Learning Mode.')

    return
# End learningMode


## randomSpeak below...
#
###
def randomSpeak(rules): 
    

# Hard coded for testing
#    rules = {
#        "S":[ 
#            ["NP", "VP"],
#            ["VP"],
#            ["AUX", "NP", "VP"]
#        ],
#        "NP":[
#            ["ProN"],
#            ["PropN"],
#            ["Det", "Nom"]
#        ],
#        "Nom":[
#            ["N", "Nom"],
#            ["N"]
#        ],
#        "ProN":[
#            ["me"],
#            ["I"],
#            ["you"],
#            ["it"]
#        ],
#        "PropN":[
#            ["John"],
#            ["Mary"],
#            ["Bob"],
#            ["Pookie"],
#            ["Pete"],
#            ["Jane"],
#            ["Sam"]
#        ],
#        "N":[ 
#            ["cat"],
#            ["dog"],
#            ["man"],
#            ["telescope"],
#            ["park"],
#            ["duck"],
#            ["bus"]
#        ],
#        "VP":[
#            ["V"],
#            ["V", "NP"],
#            ["V", "NP", "PP"],
#            ["V", "PP"],
#        ],
#        "V":[
#            ["saw"],
#            ["ate"],
#            ["walked"],
#            ["ran"],
#            ["fly"]
#        ],
#        "PP":[
#            ["Prep", "NP"]
#        ],
#        "Prep":[
#            ["in"],
#            ["on"],
#            ["by"],
#            ["with"],
#            ["at"] 
#        ],
#        "Det":[
#            ["a"],
#            ["an"],
#            ["the"],
#            ["my"],
#            ["some"]
#        ],
#        "AUX":[
#            ["can"],
#            ["could"],
#            ["might"],
#            ["will"]
#        ]
#    }


    # Contributed by Tiger Sachase
    # Used to parse any list of strings and insert them in place in a list 
    def generate_items(items):
        for item in items:
            if isinstance(item, list):
                for subitem in generate_items(item):
                    yield subitem
            else:
                yield item       

    # Our expansion algo
    def expansion(start):
        for element in start:
            if element in rules:
                loc = start.index(element)
                start[loc] = rd.choice(rules[element])
            result = [item for item in generate_items(start)]

        for item in result:
            if not isinstance(item, list):
                if item in rules:
                    result = expansion(result)
    
        return result

    # Make a string from a list
    def to_string(result):
        return ' '.join(result)

    # An example test you can run to see it at work
    result = ["S"]
#    print(result) # Print our starting result

    result = expansion(result) # Expand our starting list

    final = to_string(result)
    print(final) # Print the final result


    return final


def getInflections(w, pos):

    inflections = "No inflections found"
    # Becuse of the wonky way in whicg spacy and pyinflect work
    # we must read all base pos (NN or VB) then compare output to w
    #
##    nlp = spacy.load("en")
    nlp = spacy.load("en_core_web_sm")

    if pos == "VB":

        verbs = getVerbs() # These verbs should already be VB
        verbs = ' '.join(verbs)
        doc = nlp(verbs)

        for token in doc:
            vbd = token._.inflect("VBD")
            vbg = token._.inflect("VBG")
            vbn = token._.inflect("VBN")
            # add vbp later
            vbz = token._.inflect("VBZ")

       # print(vbd, "-", vbg, "-", vbn, "-", vbz)
        # We're assuming an inflection for each vbd, vbg, vbn, and vbz
            if w == vbd or w == vbg or w == vbn or w == vbz:
                inflections = token.text + "," + vbd + "," + vbg + "," + vbn + "," + vbz 
    elif pos == "NN":
        
#        nouns = getNouns()
#        nouns = ' '.join(nouns)


#        print("get inflec w: " + str(w))
        
        doc = nlp(w)

#        print("get inflec doc: " + str(doc))

        for token in doc:
 #           print("get inflec token.text: " + token.text)
            nns = token._.inflect("NNS")

 #           print("get inflec nns " + str(nns)) # str(nns) to handle "NoneType"
            
            if w == token.text:
                inflections = token.text + "," + str(nns)
                
        
    else:
        print("Unknown inflection pos tag: " + str(pos))

#    print("get inflec inflections: " + inflections)
    
    return inflections
# End getInflections(w, pos)


##
def getRules():

    line ="START"
    lstLine = []
    lineCnt = 0
    sList = []
    npList = []
    nomList = []
    ppList = []
    vpList = []
    advpList = []
    adjpList = []
    ccList = []
    cdList = []
    dtList = []
    inList = []
    jjList = []
    jjrList = []
    jjsList = []
    nnList = []
    nnpList = []
    nnsList = []
    mdList = []
    prpList = []
    rbList = []
    rbrList = []
    toList = []
    vbList = []
    vbdList = []
    vbgList = []
    vbnList = []
    vbpList = []
    vbzList = []
    wdtList = []

    rules = {}
    
    with open(fCFG, 'r') as fin:

        while (line := fin.readline().strip()):

            lineCnt += 1
        
            line = line.replace('-', '')
            lstLine = line.split('>')

#            print(lstLine)

            lstLine[0] = lstLine[0].replace(' ', '')

            if lstLine[0] == 'S':

                lstLine[1] = lstLine[1].lstrip()
                sList.append(lstLine[1].split())
                rules[lstLine[0]] = sList

            elif lstLine[0] == 'NP':

                lstLine[1] = lstLine[1].lstrip()
                npList.append(lstLine[1].split())

                if 'NP' in rules.keys():
                    rules[lstLine[0]] = npList
                else:
                    rules.update({"NP": lstLine[1].split()})
                
            elif lstLine[0] == 'Nom':

                lstLine[1] = lstLine[1].lstrip()
                nomList.append(lstLine[1].split())

                if 'Nom' in rules.keys():
                    rules[lstLine[0]] = nomList
                else:
                    rules.update({"Nom": lstLine[1].split()})
            elif lstLine[0] == 'PP':

                lstLine[1] = lstLine[1].lstrip()
                ppList.append(lstLine[1].split())

                if 'PP' in rules.keys():
                    rules[lstLine[0]] = ppList
                else:
                    rules.update({"PP": lstLine[1].split()})
                
            elif lstLine[0] == 'VP':

                lstLine[1] = lstLine[1].lstrip()
                vpList.append(lstLine[1].split())

                if 'VP' in rules.keys():
                    rules[lstLine[0]] = vpList
                else:
                    rules.update({"VP": lstLine[1].split()})
                
            elif lstLine[0] == 'ADVP':

                lstLine[1] = lstLine[1].lstrip()
                advpList.append(lstLine[1].split())

                if 'ADVP' in rules.keys():
                    rules[lstLine[0]] = advpList
                else:
                    rules.update({"ADVP": lstLine[1].split()})        

            elif lstLine[0] == 'ADJP':

                lstLine[1] = lstLine[1].lstrip()
                adjpList.append(lstLine[1].split())

                if 'ADVP' in rules.keys():
                    rules[lstLine[0]] = adjpList
                else:
                    rules.update({"ADJP": lstLine[1].split()})        

            elif lstLine[0] == 'CC':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                ccList.append(lstLine[1].split())

                if 'CC' in rules.keys():
                    rules[lstLine[0]] = ccList
                else:
                    rules.update({"CC": lstLine[1].split()})        

            elif lstLine[0] == 'CD':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                cdList.append(lstLine[1].split())

                if 'CD' in rules.keys():
                    rules[lstLine[0]] = cdList
                else:
                    rules.update({"CD": lstLine[1].split()})        

            elif lstLine[0] == 'DT':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                dtList.append(lstLine[1].split())

                if 'DT' in rules.keys():
                    rules[lstLine[0]] = dtList
                else:
                    rules.update({"DT": lstLine[1].split()})        

            elif lstLine[0] == 'IN':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                inList.append(lstLine[1].split())

                if 'IN' in rules.keys():
                    rules[lstLine[0]] = inList
                else:
                    rules.update({"IN": lstLine[1].split()})

            elif lstLine[0] == 'JJ':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                jjList.append(lstLine[1].split())

                if 'JJ' in rules.keys():
                    rules[lstLine[0]] = jjList
                else:
                    rules.update({"JJ": lstLine[1].split()})        

            elif lstLine[0] == 'JJR':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                jjrList.append(lstLine[1].split())

                if 'JJR' in rules.keys():
                    rules[lstLine[0]] = jjrList
                else:
                    rules.update({"JJR": lstLine[1].split()})        

            elif lstLine[0] == 'JJS':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                jjsList.append(lstLine[1].split())

                if 'JJS' in rules.keys():
                    rules[lstLine[0]] = jjsList
                else:
                    rules.update({"JJS": lstLine[1].split()})        

            elif lstLine[0] == 'NN':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                nnList.append(lstLine[1].split())

                if 'NN' in rules.keys():
                    rules[lstLine[0]] = nnList
                else:
                    rules.update({"NN": lstLine[1].split()})        

            elif lstLine[0] == 'NNP':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                nnpList.append(lstLine[1].split())

                if 'NNP' in rules.keys():
                    rules[lstLine[0]] = nnpList
                else:
                    rules.update({"NNP": lstLine[1].split()})

            elif lstLine[0] == 'NNS':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                nnsList.append(lstLine[1].split())

                if 'NNS' in rules.keys():
                    rules[lstLine[0]] = nnsList
                else:
                    rules.update({"NNS": lstLine[1].split()})        

            elif lstLine[0] == 'MD':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                mdList.append(lstLine[1].split())

                if 'MD' in rules.keys():
                    rules[lstLine[0]] = mdList
                else:
                    rules.update({"MD": lstLine[1].split()})        

            elif lstLine[0] == 'PRP':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                prpList.append(lstLine[1].split())

                if 'PRP' in rules.keys():
                    rules[lstLine[0]] = prpList
                else:
                    rules.update({"PRP": lstLine[1].split()})        

            elif lstLine[0] == 'RB':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                rbList.append(lstLine[1].split())

                if 'RB' in rules.keys():
                    rules[lstLine[0]] = rbList
                else:
                    rules.update({"RB": lstLine[1].split()})        

            elif lstLine[0] == 'RBR':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                rbrList.append(lstLine[1].split())

                if 'RBR' in rules.keys():
                    rules[lstLine[0]] = rbrList
                else:
                    rules.update({"RBR": lstLine[1].split()})        

            elif lstLine[0] == 'TO':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                toList.append(lstLine[1].split())

                if 'TO' in rules.keys():
                    rules[lstLine[0]] = toList
                else:
                    rules.update({"TO": lstLine[1].split()})        

            elif lstLine[0] == 'VB':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                vbList.append(lstLine[1].split())

                if 'VB' in rules.keys():
                    rules[lstLine[0]] = vbList
                else:
                    rules.update({"VB": lstLine[1].split()})        

            elif lstLine[0] == 'VBD':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                vbdList.append(lstLine[1].split())

                if 'VBD' in rules.keys():
                    rules[lstLine[0]] = vbdList
                else:
                    rules.update({"VBD": lstLine[1].split()})

            elif lstLine[0] == 'VBG':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                vbgList.append(lstLine[1].split())

                if 'VBG' in rules.keys():
                    rules[lstLine[0]] = vbgList
                else:
                    rules.update({"VBG": lstLine[1].split()})        

            elif lstLine[0] == 'VBN':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                vbnList.append(lstLine[1].split())

                if 'VBN' in rules.keys():
                    rules[lstLine[0]] = vbnList
                else:
                    rules.update({"VBN": lstLine[1].split()})        

            elif lstLine[0] == 'VBP':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                vbpList.append(lstLine[1].split())

                if 'VBP' in rules.keys():
                    rules[lstLine[0]] = vbpList
                else:
                    rules.update({"VBP": lstLine[1].split()})        

            elif lstLine[0] == 'VBZ':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                vbzList.append(lstLine[1].split())

                if 'VBZ' in rules.keys():
                    rules[lstLine[0]] = vbzList
                else:
                    rules.update({"VBZ": lstLine[1].split()})        

            elif lstLine[0] == 'WDT':

                lstLine[1] = lstLine[1].lstrip()
                lstLine[1] = lstLine[1].replace('"', '')
                wdtList.append(lstLine[1].split())

                if 'WDT' in rules.keys():
                    rules[lstLine[0]] = wdtList
                else:
                    rules.update({"WDT": lstLine[1].split()})        


    return rules
# End getRules()


#
def correctCase(s, NNPs):
# Capitalizes NNPs mary -> Mary

    slist = s.split(' ')
    ccs = []

    for w in slist:           
        for obj in NNPs:
            o = obj.name
            
            if o.lower() == w:
                w = w.capitalize()
                            
        ccs.append(w)

    return ccs
# End correctCase()
