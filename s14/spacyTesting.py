# Spacy testing
#
import spacy
import pickle
##import neuralcoref

print('-----')
nlp = spacy.load('en_core_web_lg')

untaggedBook = pickle.load(open('data/untaggedCorpora.p', 'rb'))

nlpDocs = []
sentCnt = 0

##neuralcoref.add_to_pipe(nlp,greedyness=0.52)

#doc = nlp('First, I wrote some sentences. Then spaCy parsed them. Hooray! Tom and Jerry ran in the park on Tuesday. They found Mark\'s baseball, and played with it.')
print('.....')
for sent in untaggedBook:
    doc = nlp(' '.join(sent))
    nlpDocs.append(doc)

##print(doc._.coref_resolved)
#print('----------------------')
#for token in doc:
    #print(type(token))
    #print(item)
#    print('----')
#    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#            token.shape_, token.is_alpha, token.is_stop)

print('=====')

#sent = next(doc.sents)
#for word in sent:
#for sent in doc.sents:
#    for word in sent:
#        print(word, word.tag_, word.dep_)
#        print(spacy.explain(word.dep_))
for doc in nlpDocs:
    sentCnt += 1
    print(sentCnt)
    print(type(doc))
    print(doc)
    print('-----')
    for word in doc:
        print(word, word.tag_, word.dep_)
        print('     ', spacy.explain(word.dep_))

pickle.dump(nlpDocs, open('data/nlpDocs.p', 'wb'))


