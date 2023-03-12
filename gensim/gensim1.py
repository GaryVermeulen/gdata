#
# Fun with Gensim -- gensim1.py
#

import pprint
from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities


text_corpus = [
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
         for document in text_corpus]

frequency = defaultdict(int)

for text in texts:
    for token in text:
        frequency[token] += 1

processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
pprint.pprint(processed_corpus)

print('-' * 5)

dictionary = corpora.Dictionary(processed_corpus)
print(dictionary)
print('-' * 5)
pprint.pprint(dictionary.token2id)


print('-' * 5)
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)

print('-' * 5)
bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
pprint.pprint(bow_corpus)

print('-' * 5)
tfidf = models.TfidfModel(bow_corpus)       # Train the model
words = "system minors".lower().split()     # Transform the "system minors" string
print(tfidf[dictionary.doc2bow(words)])

print('-' * 5)

index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=12)
query_document = 'system engineering'.split()
query_bow = dictionary.doc2bow(query_document)
sims = index[tfidf[query_bow]]
print(list(enumerate(sims)))

for document_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
    print(document_number, score)


