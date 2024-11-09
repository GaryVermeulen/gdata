#
# limitTable.py
#
# Maintain a limit table:
# Freezing Points
# Boiliong Points
# Sea Level
# ...
#

import pickle
import sys

def loadPickle():

    limits = []

    limits.append({"name": "sea_level", "min": 0.0, "max": 0.0, "units": "feet", "descriptor": "elevation;above:depth;below"}) # Starter table

    try:
        limits = pickle.load(open('limits.p', 'rb'))
        
    except FileNotFoundError:
        print("The file does not exist, using starter table.")

    return limits

def savePickle(limits):

    with open("limits.p", "wb") as f:
        pickle.dump(limits, f)
    f.close()


if __name__ == "__main__":

    limits = loadPickle()
    newLimits = []

    print('len limits: ', len(limits))
    print('type limits: ', type(limits))
    
    for l in limits:
        print("l: ", l)

    print('-----')
    action = input("Add (A), Remove (R), Exit (anything other than A or R): ")

    if action in ["A", "a"]:
        newEntry = input("Enter new limit: name, min, max, units, descriptor ")

        print(newEntry)
        print(type(newEntry))

        if len(newEntry) == 0:
            sys.exit("No entry")

        newLimit = newEntry.split(',')
    
        print(newLimit)
        print(type(newLimit))

        if len(newLimit) > 5:
            sys.exit("Too many list elements")
        elif len(newLimit) < 5:
            sys.exit("Too few list elements")

        limits.append({'name': newLimit[0], 'min': float(newLimit[1]), 'max': float(newLimit[2]), 'units': newLimit[3], 'descriptor': newLimit[4]})
    elif action in ["R", "r"]:
        
        name = input("Enter name of entry to Remove: ")
        for l in limits:
            if name == l["name"]:
                print("found--not adding to new: ", name)
            else:
                newLimits.append(l)
                
    else:
        sys.exit("Not an Add or Remove entry")
        
    print('-----')
    if len(newLimits) > 0:
        limits = newLimits
        
    for l in limits:
        print("l: ", l)

    save = input("Save to pickle <Y/n>? ")

    if save in ['Y', 'y']:
        savePickle(limits)
        print("Saved pickle file")
        

