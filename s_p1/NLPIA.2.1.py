# NLPIA.2.1.py

import numpy as np
import pandas as pd

sentence = """Thomas Jefferson began building Monticello at the age of 26."""

print("Orignal sentence:")
print(sentence)

token_sequence = str.split(sentence)
vocab = sorted(set(token_sequence))
print(', '.join(vocab))

num_tokens = len(token_sequence)
vocab_size = len(vocab)
onehot_vectors = np.zeros((num_tokens, vocab_size), int)

for i, word in enumerate(token_sequence):
    onehot_vectors[i, vocab.index(word)] = 1
print(' '.join(vocab))

print('-----')
print(onehot_vectors)

print('+++++++++++')

print(pd.DataFrame(onehot_vectors, columns=vocab))
