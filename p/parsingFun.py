#
# Parsing fun
#

import nltk


def init_wfst(tokens, grammar):
    numtokens = len(tokens)
    wfst = [[None for i in range(numtokens+1)] for j in range(numtokens+1)]
    for i in range(numtokens):
        productions = grammar.productions(rhs=tokens[i])
        wfst[i][i+1] = productions[0].lhs()
    return wfst

def complete_wfst(wfst, tokens, grammar, trace=False):
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    numtokens = len(tokens)
    for span in range(2, numtokens+1):
        for start in range(numtokens+1-span):
            end = start + span
            for mid in range(start+1, end):
                nt1, nt2 = wfst[start][mid], wfst[mid][end]
                if nt1 and nt2 and (nt1,nt2) in index:
                    wfst[start][end] = index[(nt1,nt2)]
                    if trace:
                        print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" % \
                        (start, nt1, mid, nt2, end, start, index[(nt1,nt2)], end))
    return wfst

def display(wfst, tokens):
    print('\nWFST ' + ' '.join(("%-4d" % i) for i in range(1, len(wfst))))
    for i in range(len(wfst)-1):
        print("%d   " % i, end=" ")
        for j in range(1, len(wfst)):
            print("%-4s" % (wfst[i][j] or '.'), end=" ")
        print()





groucho_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")

sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']

parser = nltk.ChartParser(groucho_grammar)

print("Chart parser:")
for tree in parser.parse(sent):
    print(tree)

# The code below exceeds depth of recursion even on this simple example
#
#rd_parser = nltk.RecursiveDescentParser(groucho_grammar) #, trace=2)
#
#print(type(rd_parser))
#print("Recursive descent parser:")
#for tree in rd_parser.parse(sent):
#    print(tree)


#prod = groucho_grammar.productions(rhs=sent[0])
print("Productions:")
#print(prod)

for i, val in enumerate(sent):
    prod = groucho_grammar.productions(rhs=sent[i])
    print(prod)


print("WFST:")
wfst0 = init_wfst(sent, groucho_grammar)
display(wfst0, sent)

wfst1 = complete_wfst(wfst0, sent, groucho_grammar) # , trace=True)
display(wfst1, sent)


