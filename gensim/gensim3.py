#
# Fun with Gensim -- gensim1.py
#

import os
import pprint
import tempfile
from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


documents = [
    "Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey",
]

new_doc = "Human computer interaction"

stoplist = set('for a of the and to in'.split(' '))

texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

frequency = defaultdict(int)

for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model

print('-' * 5)

doc_bow = [(0, 1), (1, 1)]
print(tfidf[doc_bow])
print('-' * 5)

# Or to apply a transformation to a whole corpus:
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)
print('-' * 5)

# Transformations can also be serialized, one on top of another, in a sort of chain:
lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)  # initialize an LSI transformation
corpus_lsi = lsi_model[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
print('-' * 3)
# To see the num_topices=2
lsi_model.print_topics(2)

print('-' * 5)

# both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
for doc, as_text in zip(corpus_lsi, documents):
    print(doc, as_text)
print('-' * 5)

# Model persistency is achieved with the save() and load() functions: 
with tempfile.NamedTemporaryFile(prefix='model-', suffix='.lsi', delete=False) as tmp:
    lsi_model.save(tmp.name)  # same for tfidf, lda, ...

loaded_lsi_model = models.LsiModel.load(tmp.name)
os.unlink(tmp.name)

