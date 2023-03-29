#
# grammarFun.py
#

import re
import os
import sys
import pickle
import spacy
from pathlib import Path
from buildDict import buildSentences
from collections import defaultdict # Used in Grammar class
from nltk.tree import Tree # Used in EarleyParse class
#import simpStuff as ss


class Rule(object):
    # Represents a CFG rule.

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
    # Represents a CFG.

    def __init__(self):
        # The rules are represented as a dictionary from L.H.S to R.H.S.
        self.rules = defaultdict(list)

    def add(self, rule):
        #Adds the given rule to the grammar.                
        self.rules[rule.lhs].append(rule)

    @staticmethod
    def load_grammar(fpath):
        #Loads the grammar from file

        CFGor = '|' # Currenlty not used

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

    def __getitem__(self, nt):
        # Returns the rules for a given Non-terminal.
        return self.rules[nt]

    def is_terminal(self, sym):
        # Checks is the given symbol is terminal.
        return len(self.rules[sym]) == 0

    def is_tag(self, sym):
        """
        Checks whether the given symbol is a tag, i.e. a non-terminal with rules
        to solely terminals.
        """

        if not self.is_terminal(sym):
            return all(self.is_terminal(s) for r in self.rules[sym] for s in r.rhs)

        return False


class EarleyState(object):
    # Represents a state in the Earley algorithm.

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
        # Pointers to child states (if the given state was generated using Completer).
        self.back_pointers = back_pointers

    def __eq__(self, other):
        if type(other) is EarleyState:
            return self.rule == other.rule and self.dot == other.dot and self.sent_pos == other.sent_pos

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

        return (str_helper(self) + ' (' + ', '.join(str_helper(s) for s in self.back_pointers) + ')')

    def next(self):
        # Return next symbol to parse, i.e. the one after the dot
        if self.dot < len(self):
            return self.rule[self.dot]

    def is_complete(self):
        # Checks whether the given state is complete.
        return len(self) == self.dot

    @staticmethod
    def init():
        # Returns the state used to initialize the chart in the Earley algorithm.
        return EarleyState(Rule(EarleyState.GAM, ['S']))



class ChartEntry(object):
    # Represents an entry in the chart used by the Earley algorithm.
      
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
        # Add the given state (if it hasn't already been added).
        if state not in self.states:
            self.states.append(state)



class Chart(object):
    # Represents the chart used in the Earley algorithm.
      
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
        return '\n\n'.join([("Chart[%d]:\n" % i) + str(entry) for i, entry in enumerate(self.entries)])

    @staticmethod
    def init(l):
        # Initializes a chart with l entries (Including the dummy start state).
        return Chart([(ChartEntry([]) if i > 0 else ChartEntry([EarleyState.init()])) for i in range(l)])


class EarleyParse(object):
    # Represents the Earley-generated parse for a given sentence according to a given grammar.

    def __init__(self, sentence, grammar):
        #self.words = sentence.split()
        self.words = sentence
        self.grammar = grammar
        self.chart = Chart.init(len(self.words) + 1)

    def predictor(self, state, pos):
        # Earley Predictor.
        for rule in self.grammar[state.next()]:
            self.chart[pos].add(EarleyState(rule, dot=0, sent_pos=state.chart_pos, chart_pos=state.chart_pos))

    def scanner(self, state, pos):
        # Earley Scanner.
        if state.chart_pos < len(self.words):
            word = self.words[state.chart_pos]

            if any((word in r) for r in self.grammar[state.next()]):
                self.chart[pos + 1].add(EarleyState(Rule(state.next(), [word]),
                    dot=1, sent_pos=state.chart_pos,
                    chart_pos=(state.chart_pos + 1)))

    def completer(self, state, pos):
        # Earley Completer.
        for prev_state in self.chart[state.sent_pos]:
            if prev_state.next() == state.rule.lhs:
                self.chart[pos].add(EarleyState(prev_state.rule,
                    dot=(prev_state.dot + 1), sent_pos=prev_state.sent_pos,
                    chart_pos=pos,
                    back_pointers=(prev_state.back_pointers + [state])))

    def parse(self):
        # Parses the sentence by running the Earley algorithm and filling out the chart.

        def is_tag(state):
            # Checks whether the next symbol for the given state is a tag.            
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
        # Returns the parse if it exists, otherwise returns None.
          
        def get_helper(state):
            if self.grammar.is_tag(state.rule.lhs):
                return Tree(state.rule.lhs, [state.rule.rhs[0]])

            return Tree(state.rule.lhs, [get_helper(s) for s in state.back_pointers])

        for state in self.chart[-1]:
            if state.is_complete() and state.rule.lhs == 'S' and state.sent_pos == 0 and state.chart_pos == len(self.words):
                return get_helper(state)

        return None

    



def loadPickle(whichP):

    if whichP == 'lex':
        with open('myDict.pkl', 'rb') as fp:
            newDict = pickle.load(fp)
            print('loaded dictionary pickle')
        fp.close()
        return newDict
    elif whichP == 'tWords':
        with open('taggedWords.pkl', 'rb') as fp:
            newTaggedWords = pickle.load(fp)
            print('loaded taggedWords pickle')
        fp.close()
        return newTaggedWords
    else:
        print('Unkonwn pickle name: ', whichP)

    return None


def getCFGRules():

    fRules = 'cfg_rules.cfg'    # CFG Rules w/o terminals
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


def buildCFG(lexDict): # data is now lexDict

    firstLine = True
    rules     = getCFGRules()   # CFG w/o terminals    
    fCFG      = 'simp.cfg'      # CFG w/terminals
    tagsFound = []
    
    for d in lexDict:
        word = d
        wordValue = lexDict.get(d)
        tag = wordValue["Tag"]
        
        if tag not in tagsFound:
            tagsFound.append(tag)
            
        if firstLine:
            rules = rules + tag + ' -> ' + word
            firstLine = False
        else:
            rules = rules + '\n' + tag + ' -> ' + word

    file = Path(fCFG)

    if file.is_file():
        cf = open(fCFG, 'w')
        cf.write(rules)
        cf.close()
    else:
        print("File not found: " + str(fCFG))
        sys.exit("CFG file not found")

    return tagsFound


def chkGrammar(sentence, d):

    fCFG      = 'simp.cfg'      # CFG w/terminals
    grammar = Grammar.load_grammar(fCFG)

    def run_parse(sentence):
        parse = EarleyParse(sentence, grammar)
        parse.parse()
        return parse.get()
  
    while True:
        try:

            '''
            Revist this at another time--input is assumed to be already stripped

            # Strip the sentence of any puncutation.
            stripped_sentence = sentence
            for p in string.punctuation:
                stripped_sentence = stripped_sentence.replace(p, '')

            parse = run_parse(stripped_sentence)
            '''
            parse = run_parse(sentence)
                        
            if parse is None:
                print('parse returned None for:\n\t>>' + str(sentence) + '<<\n')
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




if __name__ == "__main__":


    lexDict = loadPickle('lex')
    if lexDict == None:
        sys.exit('Bad pickle name.')
        

    print(type(lexDict))
#    print(type(taggedWords))

    for x, y in lexDict.items():
        print(x, y)

#    print('keys:')
#    for k in lexDict:
#        print(k)
#        
#        kv = lexDict.get(k)
#
#        print(kv)
#
#        tag = kv["Tag"]
#
#        print(tag)
        

#    print('-' * 9)
#
#    print('values:')
#    for v in lexDict.values():
#        print(v)
        
#    tagsFound = buildCFG(lexDict)
    
#    for t in tagsFound:
#        print(t)
#    print(len(tagsFound))

    
    sentences = buildSentences()

    print(len(sentences))

    #for s in sentences:
        #print(s)

    testSentences = sentences[110:130]

    
    print(len(testSentences))

    for s in testSentences:
        print('=' * 10)
        print(s)
        
        testSent = str(s)
        testSent = testSent.lower()
        """
        testSent = testSent.replace(',', '')
        testSent = testSent.replace('.', '')
        testSent = testSent.replace('"', ' ')
        """

        res = re.sub(r'[^\w\s]', ' ', testSent)

        #testSent = testSent.split()
        testSent = res.split()
        print(testSent)

        
    """
        draw = False
        
        grammarTree = chkGrammar(testSent, draw)

        if grammarTree == None:
            print('NONE returned, working through sentence...')

            test = []
            for w in testSent:
                test.append(w)                   
                grammarTree = chkGrammar(test, draw)
                 
                if grammarTree == None:
                    print('NONE returned for: ', test)
                else:
                    tStr = grammarTree.pformat_latex_qtree()
                    print("\n------------")
                    print('tStr:')
                    print(tStr)
                    print("\n------------")
        else:
            tStr = grammarTree.pformat_latex_qtree()
            print("\n------------")
            print('tStr:')
            print(tStr)
            print("\n------------")
                
    """
