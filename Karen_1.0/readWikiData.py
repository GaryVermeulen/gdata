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


def verifyTopic(topics, option):

    # Context?!

    if len(topics) <= 0 and option == 'w':
        print("No topics found with wildcard option (1st)")
        return None
    elif len(topics) == 0 and option == 'x':
        # Run getTopic again but with wildcard option
        topics = getTopic(topic, 'w')
        if len(topics) == 0:
            print("No topics found with wildcard option (2nd)")
            return None
    elif len(topics) > 1 and option == 'w':
        # Run getTopic again but with exact option
        topics = getTopic(topic, 'x')
        
    if len(topics) > 1:
        print('More than one topic found...')
        print('...List the first 10:')
        tCount = 0
        for t in topics:
            tCount += 1
            print(t["title"])
            if tCount > 10:
                break
    else:
        print('One topic found...')
        for t in topics:
            print(t["title"])
            print(t["text"])
        


    return "something"



if __name__ == "__main__":

    start = time.time()
    option = 'x' # Exact match, where w = wildcard
    
    print("Starting at:")
    print(datetime.datetime.now())
    print("----------")

    topic = input("Enter topic to search (CR to exit): ")
    if len(topic) == 0:
        sys.exit("Nothing entered, exiting...")

    connectMongo()
    t = getTopic(topic, option)

    v = verifyTopic(t, option)

    print('v: ', v)

    """
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
    """
    
    print("----------")
    end = time.time()
    print("\nET: ", end - start)
    print("FIN at:")
    print(datetime.datetime.now())
    
    
