#
# loopTest.py
#

verbList = ['are', 'VBP', 'done', 'VBN', 'go', 'VB', 'have', 'VB']

for x in verbList[::2]:
    print(x)

odd = True
for y in verbList:
    if odd:
        print('odd: ', y)
        word = y
        odd = False
    else:
        print('even: ', y)
        odd = True
        print('odd: {} even: {}'.format(word, y))
        
