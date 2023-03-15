#
# word2vec demo -- w2v-demo1.py
#

import gensim.downloader as api

wv = api.load('word2vec-google-news-300')

for index, word in enumerate(wv.index_to_key):
    if index == 10:
        break
    print(f"word #{index}/{len(wv.index_to_key)} is {word}")

    
### Too large to run!!!
