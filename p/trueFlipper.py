#
# test
#

inpArr = []
isTrue = True
inp = '1'
lastInp = '1'
lastTrue = '1'
trueArr = []

trueArr.append(inp)

while inp != '':

    lastInp = inp
    
    inp = input('--- Enter value: ')

    print('---')

    print(type(inp))
    print(inp)
    print(lastInp)
    print('----')

    if isTrue and (inp in trueArr):
        inpArr.append(inp)
        
        print('true: ' + str(inp))
  
    else:
        inpArr.append(inp)

        if inpArr[-3:] == [inp, inp, inp]:
            print('inp : ' + str(inp) + ' is now true')
            if inp not in trueArr:
                trueArr.append(inp)

            isTrue = True
        else:
            print('inp: ' + str(inp) + ' is false')
            isTrue = False
            
    print('-----')
    print('isTrue: ' + str(isTrue)) 
    print('inp: ' + str(inp))
    print('lastInp: ' + str(lastInp))
#    print('lastTrue: ' + str(lastTrue))
    print('inpArr:')
    print(inpArr)
    print('inArr[=3]:')
    print(inpArr[-3:])
    print('trueArr:')
    print(trueArr)

print('--- end ---')
