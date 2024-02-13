#
# accumulateKB.py
#
# Take input data and processed user input and
# make/build "accumulated" universal KBs
#

from commonUtils import connectMongo


def buildNominals():

    # Copy nnxKB to nominalsKB
    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    nominalsKB = simpDB["nominalsKB"]
    nominalsKB.drop() # Start fresh

    cursor = nnxKB.find({})

    for record in cursor:
        print(record)
        nominalsKB.insert_one(record)

    return


if __name__ == "__main__":

    buildNominals()
    
