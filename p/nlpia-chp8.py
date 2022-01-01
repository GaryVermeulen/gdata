# NLPIA
# Chp 8 RNNs
#


# 8.1
#
import glob
import os
from random import shuffle
from nltk.tokenize import TreebankWordTokenizer
from nlpia.loaders import get_data
word_vectors = get_data('wv')

# 8.2
#
def pre_process_data(filepath):
    """
    Load pos and neg examples from separate dirs then shuffle them
    together.
    """
    positive_path = os.path.join(filepath, 'pos')
    negative_path = os.path.join(filepath, 'neg')

    print('pos_path ' + str(positive_path))
    print('neg_path ' + str(negative_path))
    
    pos_label = 1
    neg_label = 0
    dataset = []
    
    for filename in glob.glob(os.path.join(positive_path, '*.txt')):
 #       print('filename ' + str(filename))
        with open(filename, 'r') as f:
            dataset.append((pos_label, f.read()))

  #  print('-----------------')
    
    for filename in glob.glob(os.path.join(negative_path, '*.txt')):
 #       print('filename ' + str(filename))
        with open(filename, 'r') as f:
            dataset.append((neg_label, f.read()))

    shuffle(dataset)
    return dataset

# 8.3
#
def tokenize_and_vectorize(dataset):
    tokenizer = TreebankWordTokenizer()
    vectorized_data = []
    for sample in dataset:
        tokens = tokenizer.tokenize(sample[1])
        sample_vecs = []
        for token in tokens:
            try:
                sample_vecs.append(word_vectors[token])
            except KeyError:
                pass
        vectorized_data.append(sample_vecs)
    return vectorized_data

# 8.4
#
def collect_expected(dataset):
    """ Peel off the target values from the dataset """
    expected = []
    for sample in dataset:
        expected.append(sample[0])
    return expected

# 8.5
#
dataset = pre_process_data('/home/gary/data/aclImdb/trains')  #"""Adjust path to correct location """

print(len(dataset))

vectorized_data = tokenize_and_vectorize(dataset)
expected = collect_expected(dataset)
split_point = int(len(vectorized_data) * .8)

x_train = vectorized_data[:split_point]
y_train = expected[:split_point]

x_test = vectorized_data[split_point:]
y_test = expected[split_point:]

# 8.6
#
maxlen = 400
batch_size = 32
embedding_dims = 300
epochs = 2

# 7.8 ###
#
def pad_trunc(data, maxlen):
    """
    For a given dataset pad with zero vectors or truncate to maxlen
    """
    new_data = []
    # Create a vector of 0s the length of our word vectors
    zero_vector = []
    for _ in range(len(data[0][0])):
        zero_vector.append(0.0)

    for sample in data:
        if len(sample) > maxlen:
            temp = sample[:maxlen]
        elif len(sample) < maxlen:
            temp = sample
            # Append the appropriate number 0 vectors to the list
            additional_elems = maxlen - len(sample)
            for _ in range(additional_elems):
                temp.append(zero_vector)
        else:
            temp = sample
        new_data.append(temp)
    return new_data

# Debug
#
print('train ' + str(len(x_train)))
print('test ' + str(len(x_test)))
print(maxlen)


# 8.7
#
print('Starting 8.7')

import numpy as np
x_train = pad_trunc(x_train, maxlen)
x_test = pad_trunc(x_test, maxlen)

print('--8.7.1--')

x_train = np.reshape(x_train, (len(x_train), maxlen, embedding_dims))
y_train = np.array(y_train)

print('--8.7.2--')

x_test = np.reshape(x_test, (len(x_test), maxlen, embedding_dims))
y_test = np.array(y_test)

print('Padding & truncation completed')

# 8.8
#
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, SimpleRNN
num_neurons = 50
model = Sequential()

print('Completed 8.8')

# 8.9
#
model.add(SimpleRNN(
    num_neurons, return_sequences=True,
    input_shape=(maxlen, embedding_dims)))

print('Completed 8.9')

# 8.10
#
model.add(Dropout(.2))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))

print('Completed 8.10')

# 8.11
#
model.compile('rmsprop', 'binary_crossentropy', metrics=['accuracy'])

model.summary()

print('----------- Completed 8.11 ------------------')

# 8.12
#
model.fit(x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(x_test, y_test))
                      
print('FINI')
