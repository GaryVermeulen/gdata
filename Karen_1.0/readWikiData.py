# Read wikiData (Mongo)
# See w2m.py
#

import pymongo
import time
import datetime
import socket
import sys

def connectMongo():

    #if socket.gethostname() == 'system76-pc':
    if socket.gethostname() == 'pop-os':
        # Home server
        #myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    else:
        # Assume work server
        #myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017")
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        
    return myclient


def getTopic(topic, option):

    records = []
    topicLC = topic.lower()

    if option not in ['w', 'x']:
        print("Unknown option: ", option)
        return records    
    
    mdb = connectMongo()
    simpDB = mdb["simp"]
    wikiData = simpDB["wikiData"]

    if option == 'w':
        topicRegex = ".*" + topicLC + ".*"
        print("topicLC = ", topicLC)
        print("topicRegex: ", topicRegex)
    
        query = {"titleLC": {"$regex": topicRegex}}
        records = list(wikiData.find(query))

    elif option == 'x':
        query = {"titleLC": topicLC}
        print("topicLC = ", topicLC)
    
        records = list(wikiData.find(query))
    else:
        print("Else: Unknown option: ", option)
        
    return records



if __name__ == "__main__":

    start = time.time()
    
    print("Starting at:")
    print(datetime.datetime.now())
    print("----------")

    topic = input("Enter topic to search (CR to exit): ")
    if len(topic) == 0:
        sys.exit("Nothing entered, exiting...")

    connectMongo()
    r = getTopic(topic, "w")

    if len(r) == 0:
        print("getTopic could not find topic: ", topic)
    else:
        if len(r) > 1:
            print("getTopic found {} on {}. ".format(len(r), topic))
            if len(r) > 100:
                print('Searching without wildcards...')
                r = getTopic(topic, "x")
                if len(r) == 0:
                    print("getTopic could not find topic: ", topic)
                else:
                    print("getTopic found the follow on topic: ", topic)
                    for t in r:
                        print(t["title"])
                        print(t["text"])
            else:
                for t in r:
                    print(t["title"])
        else:
            print("getTopic found the follow on topic: ", topic)
            for t in r:
                print(t["title"])
                print(t["text"])

    print("----------")
    end = time.time()
    print("\nET: ", end - start)
    print("FIN at:")
    print(datetime.datetime.now())
    
    
