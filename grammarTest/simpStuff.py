#
# simpStuff.py
#

import spacy # Used for inflections
import pyinflect
import sys
#import string -- used for punctuation
import os

from collections import defaultdict # Used in Grammar class
from nltk.tree import Tree # Used in EarleyParse class
from pathlib import Path

import simpConfig as sc

fRules = 'cfg_rules.cfg'    # CFG Rules w/o terminals
fCFG   = 'simp.cfg'         # CFG 
fHist  = 'rawInput.txt'     # History of raw input sentences


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

# Unused!?!?!?
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
                                                    
                    if s == tmp:
                        hist.append(lineLst)
                        
        fh.close()
    else:
        print('No history file found, created new history file.')
        fh = open(fHist, 'w')
        fh.write('# Raw input sentences without duplicates')
        fh.close()

    # if new sentence add to history
    if len(hist) < 1:

        fh = open(fHist, 'a')
        fh.write('\n' + str(s))
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

