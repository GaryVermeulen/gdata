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

verbose = True
debug   = True

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

simp = 'Simp'

validTags = [
    'CC',
    'CD',
    'DT',
    'EX',
    'FW',
    'IN',
    'JJ',
    'JJR',
    'JJS',
    'LS',
    'MD',
    'NN',
    'NNS',
    'NNP',
    'NNPS',
    'PDT',
    'POS',
    'PRP',
    'PRP$', # PRPS or PRP$
    'RB',
    'RBR',
    'RBS',
    'RP',
    'SYM',
    'TO',
    'UH',
    'VB',
    'VBD',
    'VBG',
    'VBN',
    'VBP',
    'VBZ',
    'WDT',
    'WP',
    'WP$',  # WPS or WP$
    'WRB',
    'UNK'   # My tag for unknown words
    ]

punctuationMarks = [
    '.',
    ',',
    "'",
    '"',
    '?',
    '!',
    '[',
    ']',
    '{',
    '}',
    '(',
    ')',
    '-', # dash = "--' ???
    '...',
    ':',
    ';'
    ]

validInputSentenceClassVars = [
    '_newData',
    '_type',
    '_subject',
    '_indirectSubject',
    '_verb',
    '_object',
    '_indirectObject',
    '_PRONOUNREF',
    '_PRONOUNMATCH'
    ]

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

FANBOYS = ['for', 'and', 'not', 'but', 'or', 'yet', 'so']

Determiners = ['a', 'an', 'the', 'this', 'which', 'any', 'all', 'some', 'no']

Prepositions = ['in', 'at', 'for', 'to', 'from', 'around', 'before', 'with',
                'about', 'across', 'after', 'by', 'onto', 'through', 'up',
                'above', 'below', 'between', 'inside', 'location']

subordinatingConjunctions = ['after', 'although', 'as', 'because', 'before',
                            'if', 'once', 'unless', 'since', 'so', 'that', 'though',
                            'until', 'when', 'whenever', 'where']

# Pronoun groupings--too broad and overlap...
# How are wew going to handle overlap?
#
subjectPronouns = ['I', 'You', 'you', 'He', 'he', 'She', 'she', 'It', 'it', 'We', 'we', 'They', 'they']

objectPronouns = ['Me', 'me', 'You', 'you', 'Him', 'him', 'Her', 'her', 'It', 'it', 'Us', 'us', 'Them', 'them']

possivePronouns = ['Mine', 'mine', 'Yours', 'yours', 'His', 'his', 'Hers', 'hers', 'Its', 'its', 'Ours', 'ours', 'Theirs', 'theirs']

reflexivePronouns = ['Myself', 'myself', 'Yourself', 'yourself', 'Himself', 'himself', 'Herself', 'herself', 'Itself', 'itself', 'Ourselves', 'ourselves', 'Yourselves', 'yourselves', 'Themselves', 'themselves']

# Intensive pronouns are exactly the same as reflexive pronouns, but their job in the sentence is different:
# they’re just meant to emphasize the subject of the sentence.
intensivePronouns = reflexivePronouns

demonstrativePronouns = ['This', 'this', 'That', 'that', 'These', 'these', 'Those', 'those']

interrogativePronouns = ['Who', 'who', 'What', 'what', 'Which', 'which', 'Whom', 'whom']

indefinitePronouns = ['Anyone', 'anyone', 'Someone', 'someone', 'Something', 'something', 'Nothing', 'nothing', 'All', 'all', 'Both', 'both', 'Few', 'few', 'Many', 'many', 'Several', 'several']

relativePronouns = ['Who', 'who', 'Whom', 'whom', 'Whose', 'whose', 'Which', 'which', 'That', 'that']

# Need to figure a better way
commandWords = ['No', 'no', 'Stop', 'stop', 'Do', 'do', 'Go', 'go', 'See', 'see', 'Look', 'look']

common2LetterWords = [
    'of',
    'Of',
    'to',
    'To',
    'in',
    'In',
    'it',
    'It',
    'is',
    'Is',
    'be',
    'Be',
    'as',
    'As',
    'at',
    'At',
    'so',
    'So',
    'we',
    'We',
    'he',
    'He',
    'by',
    'By',
    'or',
    'Or',
    'on',
    'On',
    'do',
    'Do',
    'if',
    'If',
    'me',
    'Me',
    'my',
    'My',
    'up',
    'Up',
    'an',
    'An',
    'go',
    'Go',
    'no',
    'No',
    'us',
    'Us',
    'am',
    'Am',
    'ok',
    'Ok',
    'OK'
    ]

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
"he'd": "he would",
"He'd": "He would",
"he'll": "he will",
"He'll": "He will",
"he's": "he is",
"He's": "He is",
"how'd": "how did",
"How'd": "How did",
"how'd'y": "how do you",
"How'd'y": "How do you",
"how'll": "how will",
"How'll": "How will",
"how's": "how is",
"How's": "How is",
"i'd": "i would",   # I'd (had) never bused so many dishes in one night
"I'd": "I would",
"i'll": "i will",
"I'll": "I will",
"i'm": "i am",
"I'm": "I am",
"i've": "i have",
"I've": "I have",
"isn't": "is not",
"Isn't": "Is not",
"it'd": "it would",
"It'd": "It would",
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
"she'd": "she would",
"She'd": "She would",
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
"that'd": "that had",
"That'd": "That had",
"that's": "that is",
"That's": "That is",
"there'd": "there would",
"There'd": "There would",
"there's": "there is",
"There's": "There is",
"they'd": "they would",
"They'd": "They would",
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
"we'd": "we would",
"We'd": "We would",
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
"where'd": "where did",
"Where'd": "Where did",
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
"you'd": "you would",
"You'd": "You would",
"you'll": "you will",
"You'll": "You will",
"you're": "you are",
"You're": "You are",
"you've": "you have",
"You've": "You have"
}

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
class inputSentence:
# inSentObj

    def __init__(self, rawSent, taggedSent, data):
        self.rawSent    = rawSent
        self.taggedSent = taggedSent
        self.data       = data

    def printAll(self):
        print('rawSent:    ', self.rawSent)
        print('taggedSent: ', self.taggedSent)
        print('data:       ', self.data)
        
        for i in validInputSentenceClassVars:
            if self.isVar(i):
                x = 'self.' + i
                print('{}   : {}'.format(i, eval(x)))

    def isVar(self, var):
        if var in self.__dir__():
            return True
        return False

    def isKnown(self, word):
        for d in self.data:
            if d[0][0] == word:
                if d[1][1] == True or d[2][1] == True or d[3][1] == True or d[4][1] == True:
                    return True
        return False


class Sentence:
    # Modified to take Spacy doc info, see S13 for original class
    # 
    def __init__(
        self,
        inputSent = None,
        taggedSentShort = None,
        taggedSentLong = None,
        epistropheSent = None,
        sType = None,
        sSubj = None,
        sVerb = None,
        sObj = None
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
        for sent in self.taggedSentShort:
            print(sent)
        print('taggedSentLong: ')
        for sent in self.taggedSentLong:
            print(sent)
        print('epistropheSent: ')
        for sent in self.epistropheSent:
            print(sent)
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
    

# Conversation context window class
class Conversation:

    def __init__(self, subject):
        #self.sentNo = sentNo
        self.subject = subject
        #self.frequency = frequency
        #self.compoundSubjects = compoundSubjects
        #self.objects = objects
        #self.indirectObjects = indirectObjects
        #self.actions = actions

    def printAll(self):
        print('sentNo           : ', self.sentNo)
        print('subject          : ', self.subject)
        print('frequency        : ', self.frequency)
        #print('compoundSubjects : ', self.compoundSubjects)
        #print('objects          : ', self.objects)
        #print('indirectObjects  : ', self.indirectObjects)
        #print('actions          : ', self.actions)

    def getSubjects(self):
        tmpLst = []
        if isinstance(self.sSubj, tuple):
            tmpLst.append(self.sSubj[0])
            return tmpLst
        elif isinstance(self.sSubj, list):
            for subjectTuple in self.sSubj:
                tmpLst.append(subjectTuple[0])
            return tmpLst
            
        return None

    def isVar(self, var):
        if var in self.__dir__():
            return True
        
        return False


class kbResults:

    def __init__(self, inSent, tagMismatch, tagMultiple, tagUnknown, subjectsInKB, subjectsNotInKB, saidBefore, simpCanX, simpAlive, subjectsCanX, subjectsAlive):
        self.inSent          = inSent
        self.tagMismatch     = tagMismatch
        self.tagMultiple     = tagMultiple
        self.tagUnknown      = tagUnknown
        self.subjectsInKB    = subjectsInKB
        self.subjectsNotInKB = subjectsNotInKB
        self.saidBefore      = saidBefore
        self.simpCanX        = simpCanX
        self.simpAlive       = simpAlive
        self.subjectsCanX    = subjectsCanX
        self.subjectsAlive   = subjectsAlive
    
    def printAll(self):
        print('inSent         : ', self.inSent)
        print('tagMismatch    : ', self.tagMismatch)
        print('tagMultiple    : ', self.tagMultiple)
        print('tagUnknown     : ', self.tagUnknown)
        print('subjectsInKB   : ', self.subjectsInKB)
        print('subjectsNotInKB: ', self.subjectsNotInKB)
        print('saidBefore     : ', self.saidBefore)
        print('simpCanX       : ', self.simpCanX)
        print('simpAlive      : ', self.simpAlive)
        print('subjectsCanX   : ', self.subjectsCanX)
        print('subjectsAlive  : ', self.subjectsAlive)
        

"""
*** DB structure for KB in MongoDB

        _id:        "String name"
        similar:    "CSV String, item, item,...,n"
        tag:        "NN" or "NNP"
        isAlive:    True or False
        canDo:      "String of simple canDo, item, item,...,n"
        superclass: "String of parent or superclass"
    
"""




    

        
    


