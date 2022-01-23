# Simple example to determine entailment in propositional logic with forward chaining
#
# This version checks each word in the input sentence aginst simpKB.txt
#

inputSentence = "Mary walked the cat in the park"

iS = ["Mary", "walked", "the", "cat", "in", "the", "park"]


# Rules are the other part of the KB that contain implications. Antecedents must be conjunctive only, and the 
# consequent must be a single atomic sentence (for the algorithm in this lab).
# Example:
#   (["looks","swims","quacks"],"duck") 
#   looks AND swims AND quacks => duck
# Indicates that if it looks like a duck, if it swims like a duck, and it quacks like a duck it must be a duck.
#rules = [(["looks","swims","quacks"],"duck"),(["barks","drules"],"dog"),(["hoots","flies"],"owl")]

fKB = 'simpKB.txt'
fMode = 'r'
f = open(fKB, fMode)

KB = {}

for line in f:
    line = line.strip('\n')
    key, value = line.split(':')
    KB[key] = value
    print(line)

f.close()

print(KB)


count = 1
    
#    print( "Starting iteration " + str(count) )

# For each rule in the set of rules ...

keyFigures = []

for key, value in KB.items():
#    print('K: ' + str(key))
#    print('I: ' + str(value))

    if key in iS:
        print('key: ' + str(key) + ' in iS: ' + str(iS))
        print(str(key) + ' can: ' + str(value))
        keyFigures.append(str(key) + ':' + str(value))

print('KF: ' + str(keyFigures))
    
#        print'p: ' + str(p))
#        antecedent, consequent = p
#
#    for key, values in rules.items():
#        print('key: ' + str(key))
#        print('value: ' + str(value))
#        antecedent, consequent = key, value
#
#        print( "Consider a rule where: " )
#        print( antecedent )
#        print( "implies: " )
#        print( consequent )
#
#        print('----------------')
#        # Determine if all chars in antecedent are also in KB
#        anteInKB = True # Flag for the antecedent in the KB
#        for q in antecedent: 
#            # q will be a list of strings
#            print(q)
#            if q not in KB: 
#                # KB is a string
#                        anteInKB = False # Flag as false, all clauses must be implied
#
#
#            
#        # If it passes the above, then antecedent should be entailed
#        if anteInKB and consequent not in KB:
#            KB.append( consequent )
#            changes = True
#            print( "Antecedent is in KB, consequent is implied, KB is now: " )
#            print(KB)
#        elif anteInKB and consequent in KB:
#            print( "Consequent is implied, but was already in KB")
#        else:
#            print( "Consequent is not implied" )
#        
#
#
#    count = count + 1
#    print("--Bottom of loop, iteration/count = " + str(count))
#
#print( "No more changes. KB is: " )
#print(KB)


print('------------')
print('FIN!')
