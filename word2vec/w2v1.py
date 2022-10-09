# Python program to generate word vectors using Word2Vec

# importing all necessary modules
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings

warnings.filterwarnings(action = 'ignore')

import gensim
from gensim.models import Word2Vec

# Reads ‘alice.txt’ file
sample = open("alice.txt")
s = sample.read()

# Replaces escape character with space
f = s.replace("\n", " ")

#print('f type: ', str(type(f)))
#print('f len:  ', str(len(f)))
#print(f[:1600])

data = []

# iterate through each sentence in the file
for i in sent_tokenize(f):
    temp = []

    # tokenize the sentence into words
    for j in word_tokenize(i):
        temp.append(j.lower())

    data.append(temp)

# Create CBOW model
model1 = gensim.models.Word2Vec(data, min_count = 1, vector_size = 100, window = 5)

print('-' * 30)

# Print results
print("Cosine similarity between 'alice' and 'wonderland' - CBOW : ", model1.wv.similarity('alice', 'wonderland'))
	
print("Cosine similarity between 'alice' and 'machines' - CBOW : ", model1.wv.similarity('alice', 'machines'))

print("Cosine similarity between 'alice' and 'laser' - CBOW : ", model1.wv.similarity('alice', 'laser'))

print("Cosine similarity between 'french' and 'mouse' - CBOW : ", model1.wv.similarity('french', 'mouse'))

print("Cosine similarity between 'algorithm' and 'laser' - CBOW : ", model1.wv.similarity('algorithm', 'laser'))

print("Cosine similarity between 'marie' and 'curie' - CBOW : ", model1.wv.similarity('marie', 'curie'))

print('-' * 30)

# Create Skip Gram model
model2 = gensim.models.Word2Vec(data, min_count = 1, vector_size = 100, window = 5, sg = 1)

# Print results
print("Cosine similarity between 'alice' and 'wonderland' - Skip Gram : ", model2.wv.similarity('alice', 'wonderland'))
	
print("Cosine similarity between 'alice' and 'machines' - Skip Gram : ", model2.wv.similarity('alice', 'machines'))

print("Cosine similarity between 'alice' and 'laser' - Skip Gram : ", model2.wv.similarity('alice', 'laser'))

print("Cosine similarity between 'french' and 'mouse' - skip gram : ", model2.wv.similarity('french', 'mouse'))

print("Cosine similarity between 'algorithm' and 'laser' - skip gram : ", model2.wv.similarity('algorithm', 'laser'))

print("Cosine similarity between 'marie' and 'curie' - skip gram : ", model2.wv.similarity('marie', 'curie'))

