#
# https://realpython.com/python-keras-text-classification/
#
from sklearn.feature_extraction.text import CountVectorizer

sentences = ['John likes ice cream', 'John hates chocolate.']

vectorizer = CountVectorizer(min_df=0, lowercase=False)
vectorizer.fit(sentences)
vv = vectorizer.vocabulary_
print(vv)

vt = vectorizer.transform(sentences).toarray()
print(vt)

