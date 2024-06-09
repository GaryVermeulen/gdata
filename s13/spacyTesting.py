# Spacy testing
#
import spacy

nlp = spacy.load('en_core_web_sm')

doc = nlp('First, I wrote some sentences. Then spaCy parsed them. Hooray!')

for token in doc:
    #print(type(token))
    #print(item)
    print('----')
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
