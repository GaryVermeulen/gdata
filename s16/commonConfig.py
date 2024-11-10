#
# commonConfig.py
#
# Global var's and classes
#
# Notes:
#    declarative sentence (statement)
#    interrogative sentence (question)
#    imperative sentence (command)
#    exclamative sentence (exclamation)
#
"""
verbose = True
debug   = True
"""
jj  = 'JJ'
jjr = 'JJR'
jjs = 'JJS'
jjx = [jj, jjr, jjs]

nn  = 'NN'
nnp = 'NNP'
nns = 'NNS'
nnps = 'NNPS'
nnx = [nn, nnp, nns, nnps]

prp  = 'PRP'
prps = 'PRP$' # PRP$
prpx = [prp, prps]

rb  = 'RB'
rbr = 'RBR'
rbs = 'RBS'

vb  = 'VB'
vbd = 'VBD'
vbg = 'VBG'
vbn = 'VBN'
vbp = 'VBP'
vbz = 'VBZ'
vbx = [vb, vbd, vbg, vbn, vbp, vbz]

wdt = 'WDT'
wp  = 'WP'
wps = 'WP$' # wps--> Cannot use: wp$
wrb = 'WRB'
whx =[wdt, wp, wps, wrb]

unk = 'UNK'

validClassVars = [
    '_indirectObject',  # Indirect object
    '_PRONOUNREF',
    '_PRONOUNMATCH',
    '_CC',
    '_CD',
    '_DT',
    '_EX',
    '_FW',
    '_IN',
    '_JJ',
    '_JJR',
    '_JJS',
    '_LS',
    '_MD',
    '_NN',
    '_NNS',
    '_NNP',
    '_NNPS',
    '_PDT',
    '_POS',
    '_PRP',
    '_PRPS', # PRP$
    '_PRPX', # Bucket for prp, prps
    '_RB',
    '_RBR',
    '_RBS',
    '_RP',
    '_SYM',
    '_TO',
    '_UH',
    '_VB',
    '_VBD',
    '_VBG',
    '_VBN',
    '_VBP',
    '_VBZ',
    '_WDT',
    '_WP',
    '_WPS',  # WP$
    '_WRB',
    '_UNK'   # My tag for unknown words
    ]

# Remove possible conflicts: I'd -> I had or I would
#
very_simple_contractions = { 
"ain't": "am not",
"Ain't": "Am not",
"aren't": "are not",
"Aren't": "Are not",
"can't": "cannot",
"Can't": "Cannot",
"'cause": "because",
"'Cause": "Because",
"could've": "could have",
"Could've": "Could have",
"couldn't": "could not",
"Couldn't": "Could not",
"didn't": "did not",
"Didn't": "Did not",
"doesn't": "does not",
"Doesn't": "Does not",
"don't": "do not",
"Don't": "Do not",
"goin'": "going",
"Goin'": "Going",
"hadn't": "had not",
"Hadn't": "Had not",
"hasn't": "has not",
"Hasn't": "Has not",
"haven't": "have not",
"Haven't": "Have not",
#"he'd": "he would", 
#"He'd": "He would",
"he'll": "he will",
"He'll": "He will",
"he's": "he is",
"He's": "He is",
#"how'd": "how did",
#"How'd": "How did",
"how'd'y": "how do you",
"How'd'y": "How do you",
"how'll": "how will",
"How'll": "How will",
"how's": "how is",
"How's": "How is",
#"i'd": "i would",   # I'd (had) never bused so many dishes in one night
#"I'd": "I would",
"i'll": "i will",
"I'll": "I will",
"i'm": "i am",
"I'm": "I am",
"i've": "i have",
"I've": "I have",
"isn't": "is not",
"Isn't": "Is not",
#"it'd": "it would",
#"It'd": "It would",
"it'll": "it will",
"It'll": "It will",
"it's": "it is",
"It's": "It is",
"let's": "let us",
"Let's": "Let us",
"ma'am": "madam",
"Ma'am": "Madma",
"mayn't": "may not",
"Mayn't": "May not",
"might've": "might have",
"Might've": "Might have",
"mightn't": "might not",
"Mightn't": "Might not",
"must've": "must have",
"Must've": "Must have",
"mustn't": "must not",
"Mustn't": "Must not",
"needn't": "need not",
"Neddn't": "Need not",
"o'clock": "of the clock",
"O'clock": "Of the clock",
"oughtn't": "ought not",
"Oughtn't": "Ought not",
"shan't": "shall not",
"Shan't": "Shall not",
"sha'n't": "shall not",
"She'n't": "Shall not",
#"she'd": "she would",
#"She'd": "She would",
"she'll": "she will",
"She'll": "She will",
"she's": "she is",
"She's": "She is",
"should've": "should have",
"Should've": "Should have",
"shouldn't": "should not",
"Shouldn't": "Should not",
"so've": "so have",
"So've": "So have",
"so's": "so is",
"So's": "So is",
#"that'd": "that had",
#"That'd": "That had",
"that's": "that is",
"That's": "That is",
#"there'd": "there would",
#"There'd": "There would",
"there's": "there is",
"There's": "There is",
#"they'd": "they would",
#"They'd": "They would",
"they'll": "they will",
"They'll": "They will",
"they're": "they are",
"They're": "They are",
"they've": "they have",
"They've": "They have",
"to've": "to have",
"To've": "They have",
"wasn't": "was not",
"Wasn't": "Was not",
#"we'd": "we would",
#"We'd": "We would",
"we'll": "we will",
"We'll": "We will",
"we're": "we are",
"We're": "We are",
"we've": "we have",
"We've": "We have",
"weren't": "were not",
"Weren't": "Were not",
"what'll": "what will",
"What'll": "What will",
"what're": "what are",
"What're": "What are",
"what's": "what is",
"What's": "what is",
"what've": "what have",
"What've": "What have",
"when's": "when is",
"When's": "When is",
"when've": "when have",
"When've": "When have",
#"where'd": "where did",
#"Where'd": "Where did",
"where's": "where is",
"Where's": "Where is",
"where've": "where have",
"Where've": "Where have",
"who'll": "who will",
"Who'll": "Who will",
"who's": "who is",
"Who's": "Who is",
"who've": "who have",
"Who've": "Who have",
"why's": "why is",
"Why's": "Why is",
"why've": "why have",
"Why've": "Why have",
"will've": "will have",
"Will've": "Will have",
"won't": "will not",
"Won't": "Will not",
"would've": "would have",
"Would've": "Would have",
"wouldn't": "would not",
"Wouldn't": "Would not",
"y'all": "you all",
"Y'all": "You all",
#"you'd": "you would",
#"You'd": "You would",
"you'll": "you will",
"You'll": "You will",
"you're": "you are",
"You're": "You are",
"you've": "you have",
"You've": "You have"
}

# Crude class for sentences
#

class Sentence:
    # Modified to take Spacy doc info, see S13 for original class
    # 
    def __init__(
        self,
        inputSent = [],
        taggedSentShort = [],
        taggedSentLong = [],
        epistropheSent = [],
        sType = [],
        sSubj = [],
        sVerb = [],
        sObj = []
        ):
        
        self.inputSent       = inputSent
        self.taggedSentShort = taggedSentShort
        self.taggedSentLong  = taggedSentLong
        self.epistropheSent  = epistropheSent
        self.type            = sType
        self.subject         = sSubj
        self.verb            = sVerb
        self.object          = sObj

    # How instances of the class are serialized and deserialized
    def __reduce__(self):
        return (self.__class__, (self.inputSent, self.taggedSentShort, self.taggedSentLong, self.epistropheSent, self.type, self.subject, self.verb, self.object))

    def printAll(self):
        print('inputSent: ', self.inputSent)
        print('taggedSentShort: ')
        for word in self.taggedSentShort:
            print(word)
        print('taggedSentLong: ')
        for word in self.taggedSentLong:
            print(word)
        print('epistropheSent: ')
        for word in self.epistropheSent:
            print(word)
        print('type     : ', self.type)
        print('subject  : ')
        for s in self.subject:
            print(s)
        print('verb     : ')
        for v in self.verb:
            print(v)
        print('object   : ')
        for o in self.object:
            print(o)
        for i in validClassVars:
            if self.isVar(i):
                x = 'self.' + i
                print('{}   : {}'.format(i, eval(x)))
                
    def isVar(self, var):
        if var in self.__dir__():
            return True

        return False

    def getSubjects(self):
        tmpLst = []
        if isinstance(self.subject, tuple):
            tmpLst.append(self.subject[0])
            return tmpLst
        elif isinstance(self.subject, list):
            for subjectTuple in self.subject:
                tmpLst.append(subjectTuple[0])
            return tmpLst
        else:
            if len(self.subject) == 0:
                return ['getSubjects: expecting tuple or list, but found nothing: ', self.subject]
            else:
                return ['getSubjects: expecting tuple or list, but found: ', self.subject]
             
        return ['No subjects to return--fall-through']

    def getSubjectsAndTags(self):
        
        if isinstance(self.subject, tuple):
            tmpLst = []
            tmpLst.append(self.subject)
            return tmpLst
        elif isinstance(self.subject, list):
            return self.subject
        else:
            if len(self.subject) == 0:
                return ['getSubjects: expecting tuple or list, but found nothing: ', self.subject]
            else:
                return ['getSubjects: expecting tuple or list, but found: ', self.subject]
            
        return ['No subjects to return--fall-through']

    def getObjectsAndTags(self):

        if isinstance(self.object, tuple):
            tmpLst = []
            tmpLst.append(self.object)
            return tmpLst
        elif isinstance(self.object, list):
            return self.object
        
        return None

    def getVerbs(self):
        tmpLst = []
        if isinstance(self.verb, tuple):
            tmpLst.append(self.verb[0])
            return tmpLst
        elif isinstance(self.verb, list):
            for verbTuple in self.verb:
                tmpLst.append(verbTuple[0])
            return tmpLst
        else:
            if len(self.verb) == 0:
                return ['getVerbs: expecting tuple or list, but found nothing: ', self.verb]
            else:
                return ['getVerbs: expecting tuple or list, but found: ', self.verb]
            
        return ['No verbs to return--fall-through']

    def getVerbsAndTags(self):

        if isinstance(self.verb, tuple):
            tmpLst = []
            tmpLst.append(self.verb)
            return tmpLst
        elif isinstance(self.verb, list):
            return self.verb
        #else:
        #    if len(self.verb) == 0:
        #        return ['getVerbs: expecting tuple or list, but found nothing: ', self.verb]
        #    else:
        #        return ['getVerbsAndTags: expecting tuple or list, but found: ', self.verb]
        #    
        #return ['No verbs/tags to return--fall-through']
        return None




    

        
    


