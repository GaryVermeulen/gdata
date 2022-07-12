#
# Simpleton
#    Simple-Ton: A ton of simple things to do.
#
#

from datetime import datetime
from dataclasses import dataclass
import simpMod as sm
import nltk
from nltk import word_tokenize

flog = 'simpLog.txt'

    

f = open(flog, 'a')
startTime = datetime.now()

print("Simple-Ton, A ton of simple things to do.")

st = startTime.strftime("%m/%d/%Y %H:%M:%S")

print('*** START RUN AT: ' + str(st) + ' ***')
f.write('\n*** START RUN AT: ' + str(st) + ' ***\n')

print("--- Reading data, one moment please ---")

inData = sm.getData()

print("----------------------")
print("--- Reading of data completed ---\n")

endTime = datetime.now()
et = endTime.strftime("%m/%d/%Y %H:%M:%S")

elpTime = endTime - startTime

print("--- endTime: " + str(et))
print("--- elapsed time: " + str(elpTime))


f.write("----------------------\n")
f.write("--- reading of data completed ---\n")
f.write("--- end time: " + str(et) + "\n")
f.write("--- elapsed time: " + str(elpTime) + "\n")
f.close()

loop = True

# Main loop
#
while loop:
   
   
    # Get user command input
    #
    cmd = sm.getInput()

    sLoopTime = datetime.now()

    if cmd == 'c' or cmd == 'C': # Chat
        s = input("Enter a short sentence: ")

    elif cmd == 's' or cmd == 'S': # Speak
        # Randomly generates a sentence from the exiting CFG
        # 
        rules = sm.getRules()
        relationFound = False
        
        while not relationFound:
            s = sm.randomSpeak(rules)
            # This check also returns a list which is needed
            ccs = sm.correctCase(s, myNames)
            pos_s = sm.getTags(s)
            relationFound = sm.searchMeaning(ccs, pos_s, myNames, myNouns)
            print('relationFound: ' + str(relationFound))
        s = ''
            
    elif cmd == 't' or cmd == 'T': # Not yet
        print("TODO: Enter learningMode")
        s = ''
    #    sm.learningMode(retCode)
    else:
        print("else cmd = " + str(cmd))
        s = ''


    # Should be left with an input sentence
    #
    if len(s) > 0: # Now the fun begins

        f = open(flog, 'a')
        
        slt = sLoopTime.strftime("%m/%d/%Y %H:%M:%S")

        print('=== START LOOP AT: ' + str(slt) + ' ===')
        f.write('\n=== START LOOP AT: ' + str(slt) + ' ===\n')
        f.close()

        # Check and correct case for NNPs
        print('Correcting case...')
        ccs = sm.correctCase(s, myNames)
        print(type(ccs))
        print(ccs)
        print('Correcting case completed.')

      

        # Parse corrected case sentenance (input) per grammar
        #
        retCode = sm.chkGrammar(ccs)

        # retCode will be either:
        # 1)
        #  retType: <class 'list'>
        #  [Tree('S', [Tree('NP', ['Mary']), Tree('VP', [Tree('V', ['walked']), Tree('NP', ['Pookie']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('N', ['park'])])])])])]
        # 2)
        #  retType: <class 'ValueError'>
        #  Grammar does not cover some of the input words: "'Harry'".
        # 3)
        #  retType: <class 'int'>
        #  0

        if retCode == 0:
            print('-->>Unable to find any productions in existing grammar')
            print('-->>Searching for relationships and/or meaning...')
            sm.searchMeaning(ccs, pos_s, myNames, myNouns)
    
        elif isinstance(retCode, ValueError):
            print('-->>retCode returned a ValueError' + str(ValueError))
            sm.myErrHandler(retCode)

# TODO           if sm.myErrHandler(retCode):
#                    sm.learningMode(retCode)
    
        elif isinstance(retCode, list):
            print('-->>Input is grammatically correct per CFG')
            print('-->>Searching for relationships and/or meaning...')

            print(retCode)
            print('- - - - - ')
            print(type(retCode))
            print('- - - - - ')
            
            sm.searchMeaning(ccs, pos_s, myNames, myNouns)
        else:
            print('-->>Something unexpected happened')
        
    else:
        loop = False

    now = datetime.now()
    elt = now.strftime("%m/%d/%Y %H:%M:%S")
    elooptime = now - sLoopTime

    f = open(flog, 'a')
    print('=== END LOOP AT: ' + str(elt) + ' ===')
    print('=== elapsed loop time: ' + str(elooptime))
    
    f.write('\n=== END LOOP AT: ' + str(elt) + ' ===\n')
    f.write('=== elapsed loop time: ' + str(elooptime) + ' ===\n')
    f.close()
        

now = datetime.now()
dt = now.strftime("%m/%d/%Y %H:%M:%S")
run_et = now - startTime

f = open(flog, 'a')    
print('*** END RUN AT: ' + str(dt) + ' ***')
print('*** elapsed run time: ' + str(run_et) + ' ***')
f.write('\n*** END RUN AT: ' + str(dt) + ' ***\n')
f.write('*** elapsed run time: ' + str(run_et) + '\n')
f.close()

print('End Simple-Ton.')

# end simp.py
