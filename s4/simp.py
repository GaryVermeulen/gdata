#
# Simpleton
#    Simple-Ton: A ton of simple things to do.
#
#

import sys
# from dataclasses import dataclass
import simpStuff as ss
#import nltk
#from nltk import word_tokenize
from datetime import datetime

flog = 'simpLog.txt'
fhistory = 'history.txt'


f = open(flog, 'a')
startTime = datetime.now()

print("Simple-Ton, A ton of simple things to do.")

st = startTime.strftime("%m/%d/%Y %H:%M:%S")

print('*** START RUN AT: ' + str(st) + ' ***')
f.write('\n*** START RUN AT: ' + str(st) + ' ***\n')

print("--- Reading data, one moment please ---")

# Read lexicon & KB data file
inData = ss.getData()

# Build CFG file from data and cfg_rules
ss.buildCFG(inData)

print("----------------------")
print("--- Reading of data completed:")

endTime = datetime.now()
et = endTime.strftime("%m/%d/%Y %H:%M:%S")

elpTime = endTime - startTime

print("    endTime: " + str(et))
print("    elapsed time: " + str(elpTime))


f.write("----------------------\n")
f.write("--- reading of data completed:\n")
f.write("    end time: " + str(et) + "\n")
f.write("    elapsed time: " + str(elpTime) + "\n")
#f.close()



loop = True

# Main loop
#
while loop:
   
   
    # Get user command input
    #
    cmd = ss.getInput()

    sLoopTime = datetime.now()

    slt = sLoopTime.strftime("%m/%d/%Y %H:%M:%S")

    print('---    START LOOP AT: ' + str(slt) + ' ===')
    f.write('\n---    START LOOP AT: ' + str(slt) + ' ===\n')


    if cmd == 'c' or cmd == 'C': # Chat
        s = input("Enter a short sentence: ")
        
        if len(s) > 0: # Now the fun begins

            # Check and correct case for NNPs
            #print('Correcting case...')
            ccs = ss.correctCase(s, inData)
            #print(type(ccs))
            print(ccs)
            print('Correcting case completed.')

            # Are all the words in the sentence in our Lex?
            ret = ss.chkWords(ccs, inData)

            if len(ret) > 0:
                # We'll do something with missing words later...
                print(len(ret))
                print(type(ret))
                print('chkWords returned: ' + str(ret))
                x = input('Shall I check external sources? <Y/N>')
                if x in ['Y', 'y']:
                    print('I shll attempt to learn on my own...')
                else:
                    print('dropping through...')
                
                continue

            # Has this been said before?
            aforementioned = ss.chkHistory(ccs)

            if len(aforementioned) > 0:
                print(len(aforementioned))
                print(type(aforementioned))
                for a in aforementioned:
                    print(a)
                    a2 = a.split(';')
                    for a2a in a2:
                        # a2a = a2a.replace(" ", "")
                        print(a2a)
                    sPOS = a2[0]
                    rel = a2[1]
                    
                saidBefore = True
            else:
                print('something new...')
                saidBefore = False

            # Parse corrected case sentence (input) per grammar
            # Draw out the grammar tree?
            draw = False
            tree = ss.chkGrammar(ccs, draw)

            if tree == None:
                validCFG = False
                print('CFG parse returned: ' + str(tree))
            else:
                validCFG = True
                print('now do something with parse tree')
                sStack = ss.getSentStack(tree)

                if len(sStack) > 0:
                    print('Sentence Stack: ' + str(sStack))
                    ss.saveStack(sStack)
                else:
                    print('No Sentence Stack returned')

            sPOS = ss.getPOS(ccs, inData)

            print('sPOS: ' + str(sPOS))
            
            rel = ss.s4m(ccs, inData, sPOS)

            if rel == None:
                relationFound = False
                print('rel = False: ' + str(rel))
            else:
                relationFound = True
                print('rel = True: ' + str(rel))

            # Thus far we can have four (4) situations:
            #   1) New sentence
            #   2) Old sentence complete KB match
            #   3) Old sentence partial KB match
            #   4) Old sentence no KB match


            
            # For now just add the new sentence   
            # Retain valid information i.e. memory or history
            if validCFG and relationFound:
                print('Saving history...')
                fh = open(fhistory, 'a')
                fh.write('\n' + str(sPOS) + '; ' + str(rel) + '; ' + slt)
                fh.close()
            else:
                print('History not saved')
                print(str(validCFG) + '; ' + str(relationFound))
            
        else:
            print('-->>Something unexpected happened')

    elif cmd == 's' or cmd == 'S': # Speak
        # Randomly generates a sentence from the exiting CFG
        # 
        rules = ss.getRules()
        relationFound = False
        
        while not relationFound:
            s = ss.randomSpeak(rules)
            # This check also returns a list which is needed
            ccs = ss.correctCase(s, inData)
            sPOS = ss.getPOS(ccs, inData)
            relationFound = ss.s4m(ccs, inData, sPOS)
            print('relationFound: ' + str(relationFound))
        s = ''
            
    elif cmd == 't' or cmd == 'T': # Tech mode; Not yet
        # Train
        #
        print("TODO: Enter learningMode")
        s = ''
    #    sm.learningMode(retCode)
    else:
        print("else cmd = " + str(cmd))
        s = ''
        loop = False

    now = datetime.now()
    elt = now.strftime("%m/%d/%Y %H:%M:%S")
    elooptime = now - sLoopTime

    f = open(flog, 'a')
    print('---    END LOOP AT: ' + str(elt) + ' ===')
    print('---    elapsed loop time: ' + str(elooptime))
    
    f.write('\n---    END LOOP AT: ' + str(elt) + ' ===\n')
    f.write('---    elapsed loop time: ' + str(elooptime) + ' ===\n')
        

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
