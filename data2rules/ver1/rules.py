# rules.py
# Dynamic rules file
#

# Example/starter rule
def isTagNNx(tag):

    if tag in ['NN', 'NNS', 'NNP']:
        return True

    return False



# New Rule: isNonfiction
def isNonfiction(functionInput):

    retVal = []
    for k in functionInput:
        if k["isNonfiction"] == True:
            retVal.append(k)

    return retVal


# New Rule: isX
def isX(isKey, kb):

    retVal = []
    for k in kb:
        if k[isKey] == True:
            retVal.append(k)

    return retVal
