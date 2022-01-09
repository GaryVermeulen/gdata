# Simple example to determine entailment in propositional logic with forward chaining

# Knowledge base is a list of propositional atomic sentences (identified by a string)
KB = ["looks","swims","quacks"]
# Rules are the other part of the KB that contain implications. Antecedents must be conjunctive only, and the 
# consequent must be a single atomic sentence (for the algorithm in this lab).
# Example:
#   (["looks","swims","quacks"],"duck") 
#   looks AND swims AND quacks => duck
# Indicates that if it looks like a duck, if it swims like a duck, and it quacks like a duck it must be a duck.
rules = [(["looks","swims","quacks"],"duck"),(["barks"],"dog"),(["hoots","flies"],"owl")]
count = 1
# Keep track of the number of times we have iterated over the whole rule set

# []: This is a list of items ...
# (): This is a tuple of items ... there is a difference  

# Keep looping, attempting to fire each rule, stopping when we loop over the whole ruleset and no new knowledge 
# is commited
changes = True
while changes:
    changes = False
    # Set the flag that there have been no changes to false
    
    print( "Starting iteration " + str(count) )

    # For each rule in the set of rules ...
    for p in rules:
        antecedent, consequent = p

        print( "Consider a rule where: " )
        print( antecedent )
        print( "implies: " )
        print( consequent )

        # Determine if all chars in antecedent are also in KB
        anteInKB = True # Flag for the antecedent in the KB
        for q in antecedent: 
            # q will be a list of strings
            if q not in KB: 
                # KB is a string
                        anteInKB = False # Flag as false, all clauses must be implied
            
        # If it passes the above, then antecedent should be entailed
        if anteInKB and consequent not in KB:
            KB.append( consequent )
            changes = True
            print( "Antecedent is in KB, consequent is implied, KB is now: " )
            print(KB)
        elif anteInKB and consequent in KB:
            print( "Consequent is implied, but was already in KB")
        else:
            print( "Consequent is not implied" )


    count = count + 1
    print("--Bottom of loop, iteration/count = " + str(count))

print( "No more changes. KB is: " )
print(KB)
