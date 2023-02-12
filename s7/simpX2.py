#
# simpX2.py 
#
import sys
import inspect
import simpConfig as sc
from simpStuff import getData
sys.path.append('/home/gary/src/s7/kb')
from simpKB import *

#
#

def extractNN(inData):

    nnLst = []
    nnpLst = []

    for i in inData:
        if len(i) == 5:
            if i[4] in ['NN']:
                nnLst.append(i)
            elif i[4] in ['NNP']:
                nnpLst.append(i)

    return nnLst, nnpLst


def undefinedClass(e):

    eList = e.split(' ')
    print('eList: ', eList)
    uClass = eList[1]
    uClass = uClass.replace("'", '')
    print('uClass: ', uClass)


    return uClass


if __name__ == "__main__":

    ''' Sample test data when running as standalone

    Input sentence w/corrected case:
    ['Mary', 'walked', 'Pookie', 'in', 'the', 'park']
    ----------------------
    sPOS =   
    sType =  declarative
    sSubj =  Mary,NNP;Pookie,NNP
    sVerb =  walked
    sObj =   park,NN
    sDet =   the
    sIN =    in
    sPP =    in,the,park,NN
    sMD =
    '''

    s = ['Mary', 'walked', 'Pookie', 'in', 'the', 'park']
    sPOS = ''
    sType = 'declarative'
    sSubj = 'Mary,NNP;Pookie,NNP'
    sVerb = 'walked'
    sObj = 'park,NN'
    sDet = 'the'
    sIN = 'in'
    sPP = 'in,the,park,NN'
    sMD = ''

    isOk = False

    print('=== simpX2 (main) ===')

    inData = getData()
    nnList, nnpList = extractNN(inData)

    sA = sc.analyzedSentence(s, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD)
    
    print('inData len: ', len(inData))
    print('inData type: ', type(inData))
    print('nnList len: ', len(nnList))
    print('nnList type: ', type(nnList))
    print('nnpList len: ', len(nnpList))
    print('nnpList type: ', type(nnpList))


    myAnimal = Animal()    
    myBird = myAnimal.prepThing("bird")
    print(f"We made a {myBird.get_name()}\n")


    myRecGround = Recreation_ground()
    myPark = myRecGround.prepThing("park")
    print(f"We made a {myPark.get_name()}\n")


    if "cat" in globals():
        print('found cat 1')
    else:
        print('cat 1 not found')

    sys.exit()

    myFeline = Feline()
    myCat = myFeline.prepThing("cat")
    print(f"We made a {myCat.get_name()}\n")


    myP_Cat = Cat()
    pookie = myP_Cat.prepThing("pookie")
    pookie.name = "Pookie"
    print(f"And POOF there is  {pookie.get_name()}\n")

    myVehicle = Vehicle()
    myCar = myVehicle.prepThing("car")
    print(f"We made a {myCar.get_name()}\n")

    if "Cat" in globals():
        print('found cat 2')
    else:
        print('cat 2 not found')



    if "bunny" in globals():
        print('bunny found')
    else:
        print('bunny not found')
        
#    try:
#        myMammal = Mammal()
#        myMammal = Animal()
#        isOk = True
#    except NameError as err:
#        print('Cannot create...')
#        print(f"err {err=}, {type(err)=}")
#        print(err)
#        undefinedClass(str(err))
#
#    if isOk:
#        myBunny = myMammal.prepThing("mammal")
#        print(f"We made a {myBunny.get_name()}\n")
#    else:
#        print('Sorry, no bunny today.')


    
    
