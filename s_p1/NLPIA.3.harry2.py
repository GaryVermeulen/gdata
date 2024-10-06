# NLPIA.3.kite.py
# NLPIA 3 kite example

from collections import Counter
from nltk.tokenize import TreebankWordTokenizer
from collections import OrderedDict
import copy
import math


def cosine_sim(vec1, vec2):
    """ Let's convert our dictionaries to lists for easier matching."""

    vec1 = [val for val in vec1.values()]
    vec2 = [val for val in vec2.values()]

    dot_prod = 0

    for i, v in enumerate(vec1):
        dot_prod += v * vec2[i]


    mag_1 = math.sqrt(sum([x**2 for x in vec1]))
    mag_2 = math.sqrt(sum([x**2 for x in vec2]))

    return dot_prod / (mag_1 * mag_2)



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

    print(doc_vectors)
    print('--------')

    document_tfidf_vectors = []
    for doc in docs:
        vec = copy.copy(zero_vector)
        tokens = tokenizer.tokenize(doc.lower())
        token_counts = Counter(tokens)
        for key, value in token_counts.items():
            docs_containing_key = 0
            for _doc in docs:
                if key in _doc:
                    docs_containing_key += 1
            tf = value / len(lexicon)
            if docs_containing_key:
                idf = len(docs) / docs_containing_key
            else:
                idf = 0
            vec[key] = tf * idf
        document_tfidf_vectors.append(vec)

    query = "How long does it take to get to the store?"
    query_vec = copy.copy(zero_vector) # book has this twice???

    tokens = tokenizer.tokenize(query.lower())
    token_counts = Counter(tokens)
    for key, value in token_counts.items():
        docs_containing_key = 0
        #for _doc in documents:
        for _doc in docs:
            if key in _doc.lower():
                docs_containing_key += 1
        if docs_containing_key == 0:
            continue
        tf = value / len(tokens)
        #idf = len(documents) / docs_containing_key
        idf = len(docs) / docs_containing_key
        query_vec[key] = tf * idf

    print(cosine_sim(query_vec, document_tfidf_vectors[0]))
    print(cosine_sim(query_vec, document_tfidf_vectors[1]))
    print(cosine_sim(query_vec, document_tfidf_vectors[2]))
    print('--------')
        
    from sklearn.feature_extraction.text import TfidfVectorizer
    corpus = docs
    vectorizer = TfidfVectorizer(min_df=1)
    model = vectorizer.fit_transform(corpus)
    print(model.todense().round(2))
    
