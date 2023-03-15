#
# word2vec demo -- w2v-demo2.py
#

from gensim.test.utils import datapath
from gensim import utils
import gensim.models
import tempfile


class MyCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __iter__(self):
        corpus_path = datapath('lee_background.cor')
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)



sentences = MyCorpus()
model = gensim.models.Word2Vec(sentences=sentences)

vec_king = model.wv['king']

print('type: ', type(vec_king))


#for index, word in enumerate(wv.index_to_key):
for index, word in enumerate(model.wv.index_to_key):
    if index == 10:
        break
    print(f"word #{index}/{len(model.wv.index_to_key)} is {word}")

    
# You can store/load models using the standard gensim methods:
with tempfile.NamedTemporaryFile(prefix='gensim-model-', delete=False) as tmp:
    temporary_filepath = tmp.name
    model.save(temporary_filepath)
    #
    # The model is now safely stored in the filepath.
    # You can copy it to other machines, share it with others, etc.
    #
    # To load a saved model:
    new_model = gensim.models.Word2Vec.load(temporary_filepath)

    
# model = gensim.models.KeyedVectors.load_word2vec_format('/tmp/vectors.txt', binary=False)
#model = gensim.models.KeyedVectors.load_word2vec_format('/tmp/vectors.bin.gz', binary=True)

big_model = gensim.models.KeyedVectors.load_word2vec_format('/home/gary/data/GoogleNews-vectors-negative300.bin.gz', binary=True)
