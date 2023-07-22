#
# simpConfig.py
#
# Global var's
#
# Notes:
#    declarative sentence (statement)
#    interrogative sentence (question)
#    imperative sentence (command)
#    exclamative sentence (exclamation)
#

verbose = True
debug   = True

nn  = 'NN'
nnp = 'NNP'
nns = 'NNS'

prp = 'PRP'

vb  = 'VB'
vbd = 'VBD'
vbg = 'VBG'
vbn = 'VBN'
vbp = 'VBP'
vbz = 'VBZ'

jj  = 'JJ'
jjr = 'JJR'
jjs = 'JJS'

unk = 'UNK'

simp = 'simp'

FANBOYS = ['for', 'and', 'not', 'but', 'or', 'yet', 'so']


extended_contractions = { 
"ain't": "am not / are not / is not / has not / have not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have",
"goin'": "going"
}


# Note case...
simple_contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"goin'": "going",
"hadn't": "had not",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"o'clock": "of the clock",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"so've": "so have",
"so's": "so is",
"that'd": "that had",
"that's": "that is",
"there'd": "there would",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"would've": "would have",
"wouldn't": "would not",
"y'all": "you all",
"you'd": "you would",
"you'll": "you will",
"you're": "you are",
"you've": "you have"
}


# Crude classes for sentences and words
#
class Sentence:

    def __init__(self, inSent, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):
        self.inSent = inSent
        self.sType = sType
        self.sSubj = sSubj
        self.sVerb = sVerb
        self.sObj = sObj
        self.sInObj = sInObj
        self.sAdj = sAdj
        self.sDet = sDet
        self.sIN = sIN
        self.sPP = sPP
        self.sMD = sMD
        self.sWDT = sWDT
        self.sCC = sCC

    def printAll(self):
        print('inSent: ', self.inSent)
        print('sType : ', self.sType)
        print('sSubj : ', self.sSubj)
        print('sVerb : ', self.sVerb)
        print('sObj  : ', self.sObj)
        print('sInObj: ', self.sInObj)
        print('sAdj  : ', self.sAdj)
        print('sDet  : ', self.sDet)
        print('sIN   : ', self.sIN)
        print('sPP   : ', self.sPP)
        print('sMD   : ', self.sMD)
        print('sWDT  : ', self.sWDT)
        print('sCC   : ', self.sCC)


class wordEntry:

    def __init__(self, word, pos, count, definition, inflections):
        self.word = word
        self.pos = pos
        self.count = count
        self.definition = definition
        self.inflections = inflections

    def printWord(self):
        print(' word       : ', self.word)
        print(' pos        : ', self.pos)
        print(' count      : ', self.count)
        print(' definition : ', self.definition)
        print(' inflections: ', self.inflections)


# Classes For an n-ary Tree KB
#
class Node:
    def __init__(self, key, children=None):
        self.key = key
        self.parentNode = ''
        self.similar = []
        self.tag = ''
        self.canDo = []
        self.children = children or []

    def __str__(self):
        return str(self.key)

    def get_childern(self):
        return self.childern


class N_ary_Tree:

    def __init__(self):
        self.root = None
        self.size = 0

    def find_node(self, node, key):
        if node == None or node.key == key:
            return node
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node
        return None

    def isNode(self, key):
        node = self.find_node(self.root, key)
        if not(node):
            return False
        else:
            return True
	
    def get_canDo(self, node, key):
        if node == None or node.key == key:
            return node.canDo
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node.canDo
        return None

    def get_parent(self, node, key):
        if node == None or node.key == key:
            return node.parentNode
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node.parentNode
        return None

    def get_similar(self, node, key):
        if node == None or node.key == key:
            return node.similar
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node.similar
        return None

    def get_tag(self, node, key):
        if node == None or node.key == key:
            return node.tag
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node.tag
        return None

    def get_children(self, node, key):
        if node == None or node.key == key:
            return node.children
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node.children
        return None


    def depth(self, key):
        node = self.find_node(self.root, key)
        if not(node):
            raise NodeNotFoundException('Depth: No element was found with the informed parent key.')
        return self.max_depth(node)

    def max_depth(self, node):
        if not(node.children):
            return 0
        children_max_depth = []
        for child in node.children:
            children_max_depth.append(self.max_depth(child))
        #return 1 + max(children_max_depth)
        return len(children_max_depth) + 1

    def add(self, new_key, similar, tag, canDo, parent_key=None):
        new_node = Node(new_key)
        new_node.similar = similar
        new_node.tag = tag
        new_node.canDo = canDo
        new_node.parentNode = parent_key
        if parent_key == None:
            self.root = new_node
            self.size = 1
        else:
            parent_node = self.find_node(self.root, parent_key)
            if not(parent_node):
                print(' ' + str(parent_key) + ' Is not a parent--cannot add: ' + new_key)
                raise NodeNotFoundException('Add: No element was found with the given parent key.')
            parent_node.children.append(new_node)
            self.size += 1

    def print_tree(self, node, str_aux):
        if node == None: return ""
        str_aux += str(node) + '('
#        print('node: ', node)
#        print(node.key)
#        print(node.children)
        for i in range(len(node.children)):
            child = node.children[i]
            end = ',' if i < len(node.children) - 1 else ''
            str_aux = self.print_tree(child, str_aux) + end
        str_aux += ')'
        return str_aux

    def is_empty(self):
        return self.size == 0

    def length(self):
        return self.size

    def __str__(self):
        return self.print_tree(self.root, "")


class NodeNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



        
    


