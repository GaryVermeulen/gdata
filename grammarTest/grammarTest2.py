#
# grammarTest2.py
#

import pathlib
import spacy


fileName = 'Corpus/MyFirstPet.txt'

nlp = spacy.load("en_core_web_sm")

doc = nlp(pathlib.Path(fileName).read_text(encoding="utf-8"))

#print([token.text for token in doc])

#sentences = list(doc.sents)
#
#print(len(sentences))
#
#for s in sentences:
#    print(s)

for token in doc:
    if str(token) != str(token.lemma_):
        print(f"{str(token):>20} : {str(token.lemma_)}")
