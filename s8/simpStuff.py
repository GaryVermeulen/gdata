#
# simpStuff.py
#
#import nltk
#from nltk import word_tokenize
#from nltk import pos_tag
import random as rd
import spacy
import pyinflect
import sys
import string
import os

from collections import defaultdict
from nltk.tree import Tree
from pathlib import Path

import simpConfig as sc

fRules = 'cfg_rules.cfg'    # CFG Rules w/o terminals
fCFG   = 'simp.cfg'         # CFG 
fLog   = 'simpLog.txt'      # Log file
fSS    = 'sentStacks.txt'   # Parsed sentences for later analysis
fHist  = 'history.txt'      # History of all sentences w/findings 

### Classes
#
class Rule(object):
        """
        Represents a CFG rule.
        """

        def __init__(self, lhs, rhs):
                # Represents the rule 'lhs -> rhs', where lhs is a non-terminal and
                # rhs is a list of non-terminals and terminals.
                self.lhs, self.rhs = lhs, rhs

        def __contains__(self, sym):
                return sym in self.rhs

        def __eq__(self, other):
                if type(other) is Rule:
                        return self.lhs == other.lhs and self.rhs == other.rhs

                return False

        def __getitem__(self, i):
                return self.rhs[i]

        def __len__(self):
                return len(self.rhs)

        def __repr__(self):
                return self.__str__()

        def __str__(self):
                return self.lhs + ' -> ' + ' '.join(self.rhs)


class Grammar(object):
        """
        Represents a CFG.
        """

        def __init__(self):
                # The rules are represented as a dictionary from L.H.S to R.H.S.
                self.rules = defaultdict(list)

        def add(self, rule):
                """
                Adds the given rule to the grammar.
                """
                
                self.rules[rule.lhs].append(rule)

        @staticmethod
        def load_grammar(fpath):
                """
                Loads the grammar from file (from the )
                """

                CFGor = '|'

                grammar = Grammar()
                
                with open(fpath) as f:
                        for line in f:
                                line = line.strip()

                                if len(line) == 0:
                                        continue

                                if line == '#':
                                        continue

                                entries = line.split('->')
                                lhs = entries[0].strip()

                                if CFGor in entries[1]:
                                        for rhs in entries[1].split('|'):
                                                grammar.add(Rule(lhs, rhs.strip().split()))
                                else:
                                        grammar.add(Rule(lhs, entries[1].strip().split()))

                return grammar

        def __repr__(self):
                return self.__str__()

        def __str__(self):
                s = [str(r) for r in self.rules['S']]

                for nt, rule_list in self.rules.iteritems():
                        if nt == 'S':
                                continue

                        s += [str(r) for r in rule_list]

                return '\n'.join(s)

        # Returns the rules for a given Non-terminal.
        def __getitem__(self, nt):
                return self.rules[nt]

        def is_terminal(self, sym):
                """
                Checks is the given symbol is terminal.
                """

                return len(self.rules[sym]) == 0

        def is_tag(self, sym):
                """
                Checks whether the given symbol is a tag, i.e. a non-terminal with rules
                to solely terminals.
                """

                if not self.is_terminal(sym):
                        return all(self.is_terminal(s) for r in self.rules[sym] for s in
                                r.rhs)

                return False


class EarleyState(object):
        """
        Represents a state in the Earley algorithm.
        """

        GAM = '<GAM>'

        def __init__(self, rule, dot=0, sent_pos=0, chart_pos=0, back_pointers=[]):
                # CFG Rule.
                self.rule = rule
                # Dot position in the rule.
                self.dot = dot
                # Sentence position.
                self.sent_pos = sent_pos
                # Chart index.
                self.chart_pos = chart_pos
                # Pointers to child states (if the given state was generated using
                # Completer).
                self.back_pointers = back_pointers

        def __eq__(self, other):
                if type(other) is EarleyState:
                        return self.rule == other.rule and self.dot == other.dot and \
                                self.sent_pos == other.sent_pos

                return False

        def __len__(self):
                return len(self.rule)

        def __repr__(self):
                return self.__str__()

        def __str__(self):
                def str_helper(state):
                        return ('(' + state.rule.lhs + ' -> ' +
                        ' '.join(state.rule.rhs[:state.dot] + ['*'] + 
                                state.rule.rhs[state.dot:]) +
                        (', [%d, %d])' % (state.sent_pos, state.chart_pos)))

                return (str_helper(self) +
                        ' (' + ', '.join(str_helper(s) for s in self.back_pointers) + ')')

        def next(self):
                """
                Return next symbol to parse, i.e. the one after the dot
                """

                if self.dot < len(self):
                        return self.rule[self.dot]

        def is_complete(self):
                """
                Checks whether the given state is complete.
                """

                return len(self) == self.dot

        @staticmethod
        def init():
                """
                Returns the state used to initialize the chart in the Earley algorithm.
                """

                return EarleyState(Rule(EarleyState.GAM, ['S']))


class ChartEntry(object):
        """
        Represents an entry in the chart used by the Earley algorithm.
        """

        def __init__(self, states):
                # List of Earley states.
                self.states = states

        def __iter__(self):
                return iter(self.states)

        def __len__(self):
                return len(self.states)

        def __repr__(self):
                return self.__str__()

        def __str__(self):
                return '\n'.join(str(s) for s in self.states)

        def add(self, state):
                """
                Add the given state (if it hasn't already been added).
                """

                if state not in self.states:
                        self.states.append(state)


class Chart(object):
        """
        Represents the chart used in the Earley algorithm.
        """

        def __init__(self, entries):
                # List of chart entries.
                self.entries = entries

        def __getitem__(self, i):
                return self.entries[i]

        def __len__(self):
                return len(self.entries)

        def __repr__(self):
                return self.__str__()

        def __str__(self):
                return '\n\n'.join([("Chart[%d]:\n" % i) + str(entry) for i, entry in
                        enumerate(self.entries)])

        @staticmethod
        def init(l):
                """
                Initializes a chart with l entries (Including the dummy start state).
                """

                return Chart([(ChartEntry([]) if i > 0 else
                                ChartEntry([EarleyState.init()])) for i in range(l)])


class EarleyParse(object):
        """
        Represents the Earley-generated parse for a given sentence according to a
        given grammar.
        """

        def __init__(self, sentence, grammar):
                #self.words = sentence.split()
                self.words = sentence
                self.grammar = grammar

                self.chart = Chart.init(len(self.words) + 1)

        def predictor(self, state, pos):
                """
                Earley Predictor.
                """

                for rule in self.grammar[state.next()]:
                        self.chart[pos].add(EarleyState(rule, dot=0,
                                sent_pos=state.chart_pos, chart_pos=state.chart_pos))

        def scanner(self, state, pos):
                """
                Earley Scanner.
                """

                if state.chart_pos < len(self.words):
                        word = self.words[state.chart_pos]

                        if any((word in r) for r in self.grammar[state.next()]):
                                self.chart[pos + 1].add(EarleyState(Rule(state.next(), [word]),
                                        dot=1, sent_pos=state.chart_pos,
                                        chart_pos=(state.chart_pos + 1)))

        def completer(self, state, pos):
                """
                Earley Completer.
                """

                for prev_state in self.chart[state.sent_pos]:
                        if prev_state.next() == state.rule.lhs:
                                self.chart[pos].add(EarleyState(prev_state.rule,
                                        dot=(prev_state.dot + 1), sent_pos=prev_state.sent_pos,
                                        chart_pos=pos,
                                        back_pointers=(prev_state.back_pointers + [state])))

        def parse(self):
                """
                Parses the sentence by running the Earley algorithm and filling out the
                chart.
                """

                # Checks whether the next symbol for the given state is a tag.
                def is_tag(state):
                        return self.grammar.is_tag(state.next())

                for i in range(len(self.chart)):
                        for state in self.chart[i]:
                                if not state.is_complete():
                                        if is_tag(state):
                                                self.scanner(state, i)
                                        else:
                                                self.predictor(state, i)
                                else:
                                        self.completer(state, i)

        def has_parse(self):
                """
                Checks whether the sentence has a parse.
                """

                for state in self.chart[-1]:
                        if state.is_complete() and state.rule.lhs == 'S' and \
                                state.sent_pos == 0 and state.chart_pos == len(self.words):
                                return True

                return False

        def get(self):
                """
                Returns the parse if it exists, otherwise returns None.
                """

                def get_helper(state):
                        if self.grammar.is_tag(state.rule.lhs):
                                return Tree(state.rule.lhs, [state.rule.rhs[0]])

                        return Tree(state.rule.lhs,
                                [get_helper(s) for s in state.back_pointers])

                for state in self.chart[-1]:
                        if state.is_complete() and state.rule.lhs == 'S' and \
                                state.sent_pos == 0 and state.chart_pos == len(self.words):
                                return get_helper(state)

                return None
# End Classes

################################################
# Currently words are within POS files, and only
# nouns (NN, NNP, and NNS contain any kind of knowledge
#
def getData():

    dataList = []
    progPath = os.getcwd()
    dataPath = progPath + '/data'
    dirList = os.listdir(dataPath)

    for inFile in dirList:
        with open(dataPath + '/' + inFile, 'r') as f:
            while (line := f.readline().rstrip()):
                if '#' not in line:
                    line = line.replace(' ', '')
                    line = line.split(";")

                    if line[0] != '#':
                        line.append(inFile.upper()) # Add POS tag from file name
                        dataList.append(line)
    f.close()

    return dataList

# End getData

################################################
def getCFGRules():

    rules = ''

    progPath = os.getcwd()
    dataPath = progPath + '/cfg'

    file = Path(dataPath + '/' + fRules)

    if file.is_file():

        rf = open(dataPath + '/' + fRules, 'r') # Get base rules
        rules = rf.read()
        rf.close()
    else:
        print("File not found: " + str(dataPath + '/' + fRules))
        sys.exit("CFG Rules file not found")

    return(rules)
# End getRules

################################################
# f = noun file
# n = noun data
#
def getNx(f, n):

    Nx = ' ' + str(n) + ' Not Found'
    progPath = os.getcwd()
    dataPath = progPath + '/data'
    
    file = Path(dataPath + '/' + f)

    if file.is_file():

        with open(file, 'r') as fin:
        
            while (line := fin.readline().rstrip()):
                if '#' not in line:
                    line = line.replace(' ', '') # Needed?
                    line = line.split(";")
                    
                    if line[0] == n:
                        Nx = line

        fin.close()
    else:
        print("File not found: " + str(n))
        sys.exit("inData file not found")

    return(Nx)
# End getNx

################################################
def buildCFG(data):

    rules = getCFGRules()

    firstLine = True
    
    for d in data:
        if firstLine:
            rules = rules + d[1] + ' -> ' + d[0]
            firstLine = False
        else:
            rules = rules + '\n' + d[-1] + ' -> ' + d[0]

    file = Path(fCFG)

    if file.is_file():
        cf = open(fCFG, 'w')
        cf.write(rules)
        cf.close()
    else:
        print("File not found: " + str(fCFG))
        sys.exit("CFG file not found")

    return
# End buildCFG

################################################
def getInput():

    s = input("Enter a command <[C]hat, [S]peak, or [T]each>: ")

    if s == 'c' or s == 'C':
        if sc.verbose: print(s)
        print("Entering Chat mode...")
    elif s == 's' or s == 'S':
        if sc.verbose: print(s)
        print("Entering random Speak mode...")
    elif s == 't' or s == 'T':
        if sc.vervose: print(s)
        print("Entering Teach mode...")
    else:
        print("I do not understand: >>" + str(s) + "<<")

    return s
# end getInput

################################################
# Capitalizes NNPs mary -> Mary
#
def correctCase(s, data):

    slist = s.split(' ')
    ccs = []

    for w in slist:           
        for d in data:
                       
            if d[0].lower() == w:
                if d[-1] == 'NNP':
                    w = w.capitalize()
                            
        ccs.append(w)

    return ccs
# End correctCase

################################################
def chkWords(s, inData):
# Returns sentence words not in lex
    words = []

    for d in inData:
        words.append(d[0])
                
    s1 = set(s)
    s2 = set(words)
    ret = s1.difference(s2)
    
    return ret
# End chkWords

################################################
def chkGrammar(sentence, d):

    grammar = Grammar.load_grammar(fCFG)

    def run_parse(sentence):
        parse = EarleyParse(sentence, grammar)
        parse.parse()
        return parse.get()
  
    while True:
        try:

            '''
            Revist this at another time

            # Strip the sentence of any puncutation.
            stripped_sentence = sentence
            for p in string.punctuation:
                stripped_sentence = stripped_sentence.replace(p, '')

            parse = run_parse(stripped_sentence)
            '''
            parse = run_parse(sentence)
                        
            if parse is None:
                if sc.verbose: print('parse returned None for:\n\t' + str(sentence) + '\n')
                return(parse)
            else:
                if d:
                    parse.draw()
                else:
                    parse.pretty_print()

            return(parse)
        except EOFError:
            return('EOFError')
    
    return('Drop-through-parse-error')

# end chkGrammar(s)

################################################
def tree2List(t):

    tStr = t.pformat_latex_qtree()

    tList = tStr.split('\n')

    return(tList)
#End tree2List

################################################
def saveStack(s):
# Build a history of sentences for later analysis

    #inStr = '\n' + str(s)
    inStr = str(s)
    inStr = inStr.strip('\n')

    sf = open(fSS, 'a')
    sf.write(inStr + '\n')
    sf.close()
# End saveStack

################################################
def getPOS(s, data):

    sPOS = []
    
    for w in s:
        for d in data:
            if w == d[0]:
                sPOS.append((w,d[1]))
    return(sPOS)
# End getPOS

################################################
def getInflections(w, pos):

    inflections = "No inflections found"
    #inflections = w # If no inflections found return original
    
    # Becuse of the wonky way in which spacy and pyinflect work
    # we must read all base pos (NN or VB) then compare output to w
    #
##    nlp = spacy.load("en")
    nlp = spacy.load("en_core_web_sm")

    if pos == "VB":

        doc = nlp(w)

        for token in doc:
            vb  = token._.inflect("VB")
            vbd = token._.inflect("VBD")
            vbg = token._.inflect("VBG")
            vbn = token._.inflect("VBN")
            # add vbp later
            vbz = token._.inflect("VBZ")

            # We're assuming an inflection for each vbd, vbg, vbn, and vbz
            if w == vb or w == vbd or w == vbg or w == vbn or w == vbz:
                #inflections = token.text + "," + vb + "," + vbd + "," + vbg + "," + vbn + "," + vbz
                inflections = vb + "," + vbd + "," + vbg + "," + vbn + "," + vbz 
    elif pos == "NN":
        
        doc = nlp(w)

        for token in doc:
            nn  = token._.inflect("NN")
            nns = token._.inflect("NNS")
            
            if w == nn or w == nns:
                inflections = nn + "," + nns        
    else:
        print("Unknown inflection pos tag: " + str(pos))
    
    return inflections
# End getInflections


################################################
def chkHistory(s):

    sSet = set(s)
    hist = []
    file = Path(fHist)

    if file.is_file():

        fh = open(fHist, 'r')
        myHist = fh.read()
        fh.close()

        lines = myHist.split('\n')

        for line in lines:
            
            if len(line) > 0:
                if line[0] != '#':
                    lineLst = line.split(';')

                    # Rough-hewn, but readable
                    tmp = lineLst[0].replace('[', '')
                    tmp = tmp.replace(']', '')
                    tmp = tmp.replace(' ', '')
                    tmp = tmp.replace("'", "")
                    tmp = tmp.split(',')

                    tmpSet = set(tmp)

                    if sSet == tmpSet:
                        hist.append(lineLst)
    else:
        print('No history file found, created new history file.')
        fh = open(fHist, 'w')
        fh.write('# Input sentence, Possible relationships, Date; Time')
        fh.close()
    
    return hist
# End chkHistory

################################################
def removePOS(sPOS):

    noPOS = []
    
    s = sPOS.strip("[])(")
    s = s.replace("(", "") # strip does not remove all ( or )
    s = s.replace(")", "")
    s = s.replace("'", "")
    s = s.replace(" ", "")

    s = s.split(',')

    # the second item is POS so just skip it
    i = 0
    while i < len(s):
        noPOS.append(s[i])
        i = i + 2
    
    return noPOS
# End removePOS

################################################
def addWord(nw):

    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup
    import nltk

    found = False
    r = False
    notFound = []
    foundLst = []
    
    print('Entering addWord: ')

    nwList = list(nw)

    print('Verifying spelling...')

    for w in nwList:        
        wLst = []
        req = Request(
            url = "https://www.vocabulary.com/dictionary/" + w + "",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        htmlFile = urlopen(req).read()
        soup = BeautifulSoup(htmlFile, 'html.parser')

        soup1 = soup.find(class_="short")
        try:
            soup1 = soup1.get_text()
            found = True
        except AttributeError:
            print('Cannot find such word!')
            print(w)
            print('Check spelling.')
            notFound.append(w)
            found = False
            continue
        if found:
            
            soup2 =soup.find(class_="word-definitions")
            txt = soup2.get_text()
            txt = os.linesep.join([s for s in txt.splitlines() if s])
            txtLst = txt.split('\n')

            if sc.verbose:
                print('Found: ' + str(w))
                print('soup: ', soup1)
                print('txtLst[1]: ', txtLst[1])

        wLst.append(w)
        wTag = nltk.pos_tag(wLst) # WARNING: nltk can return incorrect results!

        if wTag[0][1] in ['NN', 'NNS']:
            i = (getInflections(wTag[0][0], 'NN'))
        elif wTag[0][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBZ']:
            i = (getInflections(wTag[0][0], 'VB'))
        else:
            i = "No Inflection Found"
            print('No Inflection Found for wTag: ' + str(wTag))

        foundLst.append(w + ';' + str(wTag[0][1]) + ';' + str(txtLst[1]) + ';' + i + ';' + soup1)

    if sc.verbose: 
        print('foundLst: ', str(foundLst))
        print('-f-' * 5)
    
    for f in foundLst:

        fLst = f.split(';')

        if sc.verbose: 
            print('f: ', f)
            print('fLst: ', str(fLst))
        
        cp = chkPOS(f)
        if sc.verbose: print(str(cp))
        
        if cp:
            print('We can add:')
            print(f)
            res = input('Add to data? <Y/y>')

            if res in ['Y','y']:
                print('add')
                r = addWord2File(fLst[0], fLst[1])
            else:
                print('do not add')
                r = False

        else:
            print('Found mismatch with POS tag: ' + str(fLst[1]) + ' and dictionary: ' + str(fLst[2]))
            print(f)

    if sc.verbose: print('-n-' * 5)
    for n in notFound:
        if sc.verbose: print('n {}'.format(n))

    if r:
        print('res retunred true--meaning word added')

    print('End addWord.')
      
    return r
# End addWord()

################################################
def chkPOS(d):
    posMatch = False

    print('----- chkPos -----')
    if sc.verbose: 
        print(type(d))
        print(d)

    dLst = d.split(';')

    if sc.verbose: print('dLst: ', str(dLst))

    nouns = ['NNS','NN','NNP']
    verbs = ['VB','VBG','VBD','VBN','VBZ']
    adjectives = ['JJ','JJR','JJS']
    modals = ['MD']
    personal_pronouns = ['PRP']
    adverbs = ['RB','RBR','RBS']

    if dLst[2] == 'adjective':
        if dLst[1] in adjectives:
            posMatch = True
    elif dLst[2] == 'noun':
        if dLst[1] in nouns:
            posMatch = True
    elif dLst[2] == 'verb':
        if sc.verbose: print('*** here')
        if dLst[1] in verbs:
            if sc.verbose: print('*** there')
            posMatch = True
    elif dLst[2] == 'adverb':
        if dLst[1] in adverbs:
            posMatch = True

    if sc.verbose: 
        print('   dLst[2]: >>' + str(dLst[2]) + '<<')
        print('   dLst[1]: ', str(dLst[1]))

    print('   posMatch:', str(posMatch))

    print('--- End chkPos ---')
    return posMatch
# End chkPOS(d)

################################################
def addWord2File(w, posTag):

    print('--- addWord2File ---')

    success = False
    
    progPath = os.getcwd()
    dataPath = progPath + '/data'

    file = Path(dataPath + '/' + posTag.lower())

    if file.is_file():
        if sc.verbose: print('   file found: ', file)
        f = open(file, 'a')
        f.write(w + '\n')
        f.close()
        success = True
    else:
        success = False
        
    print('--- End addWord2File ---')
    return success
# End addWord2File(w, posTag)












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

