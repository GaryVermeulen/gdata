#
# Spacy POS tagging
#
import spacy

sp = spacy.load('en_core_web_sm')

sen = sp(u"do you see bob")

print(sen.text)

for word in sen:
    print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
    
