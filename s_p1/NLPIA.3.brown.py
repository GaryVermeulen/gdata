# NLPIA.3.kite.py
# NLPIA 3 kite example

import nltk
from collections import Counter
#nltk.download('brown') # May not need to download
from nltk.corpus import brown


#
if __name__ == "__main__":

    puncs = set((',', '.', '--', '-', '!', '?', ':', ';', '``', "''", '(', ')', '[', ']'))

    print(brown.words()[:10])
    print(brown.tagged_words()[:5])
    
    print(len(brown.words()))

    word_list = (x.lower() for x in brown.words() if x not in puncs)
    token_counts = Counter(word_list)
    print(token_counts.most_common(20))
