#
# kbEdit.py
#


def chk_nominalsKB(item, nominalsKB):

    print('chk_nnxKB looking for: ', item)
    
    query = {"_id": item}
    records = list(nominalsKB.find(query))

    if len(records) < 1:
        print('KB item: {} not found in KB.'.format(item))
        return {}
    else:
        if len(records) == 1:
            return records[0]
        else:                
            print('{} records found for {} where we should have only one...~?'.format(len(records), item))
            return {}            
        
    # End chk_nnxKB


def modKB(item, nominalsKB):

    print('start modKB item: ', item)
    #keys = item.keys()

    
    key = input('Enter key to modify or add: ')
    val = input('New value for key: ')

    item.update({key: val})

    print('-' * 5)
    print('after modKB item: ', item)
    
    print('ModKB complete')

    return item
    

"""
From processInput.py for reference


def kbCommand(nnxKB):

    nodeKey = input('Enter KB Node (key/name) to display: ')

    node = nnxKB.find({"_id":nodeKey})

    if node == None:
        print('Could not find a node named: ', nodeKey)
    else:
        print('node: ', node)
        for item in node:
            print('item: ', item)
    
    chkKB_Results = chk_nnxKB(nodeKey, nnxKB)
    if len(chkKB_Results) > 0:
        print('-' * 5)
        print(chkKB_Results)
        print(chkKB_Results["_id"])
        print(chkKB_Results["similar"])
        print(chkKB_Results["tag"])
        print(chkKB_Results["isAlive"])
        print(chkKB_Results["canDo"])
        print(chkKB_Results["superclass"])
    
    return

"""
