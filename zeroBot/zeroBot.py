#
# zeroBot.py
#

import socket
import pymongo

def connectMongo():

    if socket.gethostname() == 'system76-pc':
        # Home server
        myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")
    else:
        # Assume work server
        myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017")

    return myclient




#
if __name__ == "__main__":

    cease = False
    inputs = []

    mdb = connectMongo()
    zeroDB = mdb["zero"]
    zeroCol = zeroDB["zeroCol"]

    print("Hi, I am zeroBot I only know what you say.")

    while not cease:

        userInput = input("Please say something: ").lower()

        if len(userInput) < 1:
            break

        q = {"userinput": userInput}

        records = list(zeroCol.find(q))

        if len(records) < 1:
            print("Sorry, I have never heard of that.")
            zeroCol.insert_one({"userinput":userInput})
        else:
            for r in records:
                print("I have heard of that:")
                print(r)

        

        
