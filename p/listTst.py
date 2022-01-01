#!/usr/bin/env python3

messages = [b"Message 1 from client.", b"Message 2 from client."]

def popMsgs(messages):

    print("type:   " + str(type(messages)))
    print("len:    " + str(len(messages)))
    print("pop(0): " + str(messages.pop(0)))
    print("len:    " + str(len(messages)))
    print("pop(0): " + str(messages.pop(0)))
    print("len:    " + str(len(messages)))
    
def myFunction(messages):
    popMsgs(messages)
    
myFunction(messages)
    
    
