#
# Sentence Analysis Testing
#
# Sample sentence tree inputs:

import simpSAx as sa

"""

\Tree [.S [.VP [.VB walk ] ] ]

\Tree [.S [.VP [.VB see ] [.NP [.NNP Bob ] ] ] ]

\Tree [.S [.VP [.VB see ] [.NP [.NN cat ] ] ] ]

\Tree [.S [.VP [.VBG running ] [.NP [.NNP Pookie ] ] ] ]

\Tree [.S [.VP [.VB see ] [.NP [.DT the ] [.NN cat ] ] ] ]

\Tree [.S [.VP [.VB see ] [.NP [.DT the ] [.NNP Pookie ] ] ] ]

\Tree [.S [.NP [.NNP Bob ] ] [.VP [.VBZ sees ] ] ]

\Tree [.S
        [.NP [.NNP Bob ] ]
        [.VP [.VBD saw ] [.NP [.DT the ] [.NN cat ] ] ] ]
        
\Tree [.S
        [.NP
          [.NP [.NNP Bob ] ]
          [.VP [.VBD saw ] [.NP [.DT the ] [.NN cat ] ] ] ]
        [.VP [.VB eat ] [.NP [.DT the ] [.NN duck ] ] ] ]        

\Tree [.S [.NP [.NN duck ] ] [.VP [.VBZ eats ] ] ]

\Tree [.S [.NP [.NNS ducks ] ] [.VP [.VB eat ] ] ]

\Tree [.S [.NP [.NNS telescopes ] ] [.VP [.VB fly ] ] ]

\Tree [.S [.NP [.DT the ] [.NN cat ] ] [.VP [.VBZ runs ] ] ]


\Tree [.S
        [.VP [.VB see ] [.NP [.NP [.NNP Bob ] ] [.VP [.VB run ] ] ] ] ]

\Tree [.S
        [.VP
          [.VB see ]
          [.NP
            [.NP [.NP [.NNP Bob ] ] [.VP [.VB run ] ] ]
            [.PP [.IN in ] [.NP [.DT the ] [.NN park ] ] ] ] ] ]

\Tree [.S
        [.NP [.NNP Mary ] ]
        [.VP
          [.VBN walked ]
          [.NP [.NNP Pookie ] ]
          [.PP [.IN in ] [.NP [.DT the ] [.NN park ] ] ] ] ]

\Tree [.S
        [.NP [.DT the ] [.NN telescope ] ]
        [.VP [.VBD ate ] [.NP [.DT the ] [.NN park ] ] ] ]
        
\Tree [.S
        [.NP [.PRP I ] ]
        [.VP
          [.VBD saw ]
          [.NP
            [.NP
              [.NP [.NNP Pookie ] ]
              [.PP [.IN in ] [.NP [.DT the ] [.NN park ] ] ] ]
            [.PP [.IN with ] [.NP [.DT a ] [.NN telescope ] ] ] ] ] ]
            
\Tree [.S
        [.NP [.PRP I ] ]
        [.VP
          [.VBD saw ]
          [.NP
            [.NP
              [.NP [.DT a ] [.NN duck ] ]
              [.PP [.IN in ] [.NP [.DT the ] [.NN park ] ] ] ]
            [.PP [.IN with ] [.NP [.DT a ] [.NN telescope ] ] ] ] ] ]
            
"""

inSent1 = '\Tree [.S [.VP [.VB see ] [.NP [.DT the ] [.NNP Pookie ] ] ] ]'

inSent2 = '''\Tree [.S
        [.NP [.NNP Bob ] ]
        [.VP [.VBD saw ] [.NP [.DT the ] [.NN cat ] ] ] ]
'''

inSent3 = '''\Tree [.S
        [.NP [.PRP I ] ]
        [.VP
          [.VBD saw ]
          [.NP
            [.NP
              [.NP [.DT a ] [.NN duck ] ]
              [.PP [.IN in ] [.NP [.DT the ] [.NN park ] ] ] ]
            [.PP [.IN with ] [.NP [.DT a ] [.NN telescope ] ] ] ] ] ]
'''

flog = 'simpLog.txt'
f = open(flog, 'a')

print('---')

inSentLst = inSent1.split('\n')

print(type(inSentLst))
print(len(inSentLst))

for line in inSentLst:
    print(line)
    
print('---')

# Orginal from simp.py
#
# sAnaly = sa.sentAnalysis(tList, f)
#

sAnaly = sa.sentAnalysis(inSentLst, f)

print('sAnaly:')
print(sAnaly)
print('\n---End---')

