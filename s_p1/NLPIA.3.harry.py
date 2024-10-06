# NLPIA.3.kite.py
# NLPIA 3 kite example

from collections import Counter
from nltk.tokenize import TreebankWordTokenizer
from collections import OrderedDict
import copy



#
if __name__ == "__main__":

    docs = ["The faster Harry got to the store, the faster and faster Harry would get home."]
    docs.append("Harry is hairy and faster than Jill.")
    docs.append("Jill is not as hairy as Harry.")
    
    # kite example
    tokenizer = TreebankWordTokenizer()
    """
    tokens = tokenizer.tokenize(kite_text.lower())
    token_counts = Counter(tokens)
    print(token_counts)
    """
    # harry example
    #print(docs)
    doc_tokens = []
    for doc in docs:
        doc_tokens += [sorted(tokenizer.tokenize(doc.lower()))]

    print(len(doc_tokens[0]))

    all_doc_tokens = sum(doc_tokens, [])
    print(len(all_doc_tokens))

    lexicon = sorted(set(all_doc_tokens))
    print(len(lexicon))
    
    zero_vector = OrderedDict((token, 0) for token in lexicon)
    
    doc_vectors = []
    for doc in docs:
        vec = copy.copy(zero_vector)
        tokens = tokenizer.tokenize(doc.lower())
        token_counts = Counter(tokens)
        for key, value in token_counts.items():
            vec[key] = value / len(lexicon)
        doc_vectors.append(vec)
        
            
