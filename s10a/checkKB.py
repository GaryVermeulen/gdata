#
# checkKB.py
#

import pickle

from commonUtils import loadPickle
from commonUtils import savePickle

from simpConfig import Node
from simpConfig import N_ary_Tree
from simpConfig import NodeNotFoundException



if __name__ == "__main__":

    print(' --- checkKB ---')

    testName = 'pookie'

    kbTree = loadPickle('kbTree')


    print(kbTree.print_tree(kbTree.root, ''))

    canDo = kbTree.get_canDo(kbTree.root, testName)
    ppt = kbTree.get_ppt(kbTree.root, testName)
    tag = kbTree.get_tag(kbTree.root, testName)
    children = kbTree.get_children(kbTree.root, testName)
    
    print('---')
    print('{} can: {}'.format(testName, canDo))
    print(ppt)
    print(tag)
    print('childern of {}:'.format(testName))
    for c in children:
        print(c.key)

    print('parents of {}:'.format(testName))
    p = testName
    while p != None:
        oldP = p
        p = kbTree.get_parent(kbTree.root, p)
        if p == None:
            print('{} is god/root'.format(oldP))
        else:
            print('parent of {} is {}'.format(oldP, p))

    print('---')

    node = kbTree.find_node(kbTree.root, testName)

    print('node.key: ', node.key)
    print('--- Add, rodent, hamster, and hammy')
    

    # Test add new node
    #
    newNode = 'rodent'
    ppt = 't'
    tag = 'NN'
    canDO = 'see,eat,walk,run'
    newNodeParent = 'mammal' # which is a rodent which is a mammal
    
    # Does parnet class exist?
    node = kbTree.find_node(kbTree.root, newNodeParent)
    if node == None:
        print('Parent node not found.')
    else:
        print('Adding: ', newNode, ppt, tag, canDo, newNodeParent)
        kbTree.add(newNode, ppt, tag, canDo, newNodeParent)
        

    # Add many children for rodentx test
    #
    newNode = 'rat'
    ppt = 't'
    tag = 'NN'
    canDO = 'see,eat,walk,run'
    newNodeParent = 'rodent' # which is a rodent which is a mammal

    # Does parnet class exist?
    node = kbTree.find_node(kbTree.root, newNodeParent)
    if node == None:
        print('Parent node not found.')
    else:
        print('Adding: ', newNode, ppt, tag, canDo, newNodeParent)
        kbTree.add(newNode, ppt, tag, canDo, newNodeParent)


    newNode = 'mouse'
    ppt = 't'
    tag = 'NN'
    canDO = 'see,eat,walk,run'
    newNodeParent = 'rodent' # which is a rodent which is a mammal

    # Does parnet class exist?
    node = kbTree.find_node(kbTree.root, newNodeParent)
    if node == None:
        print('Parent node not found.')
    else:
        print('Adding: ', newNode, ppt, tag, canDo, newNodeParent)
        kbTree.add(newNode, ppt, tag, canDo, newNodeParent)


    newNode = 'squirrel'
    ppt = 't'
    tag = 'NN'
    canDO = 'see,eat,walk,run'
    newNodeParent = 'rodent' # which is a rodent which is a mammal

    # Does parnet class exist?
    node = kbTree.find_node(kbTree.root, newNodeParent)
    if node == None:
        print('Parent node not found.')
    else:
        print('Adding: ', newNode, ppt, tag, canDo, newNodeParent)
        kbTree.add(newNode, ppt, tag, canDo, newNodeParent)

    
    newNode = 'hamster'
    ppt = 't'
    tag = 'NN'
    canDO = 'see,eat,walk,run'
    newNodeParent = 'rodent' # which is a rodent which is a mammal

    # Does parnet class exist?
    node = kbTree.find_node(kbTree.root, newNodeParent)
    if node == None:
        print('Parent node not found.')
    else:
        print('Adding: ', newNode, ppt, tag, canDo, newNodeParent)
        kbTree.add(newNode, ppt, tag, canDo, newNodeParent)


    newNode = 'hammy'
    ppt = 't'
    tag = 'NNP'
    canDO = 'see,eat,walk,run'
    newNodeParent = 'hamster' # which is a rodent which is a mammal

    # Does parnet class exist?
    node = kbTree.find_node(kbTree.root, newNodeParent)
    if node == None:
        print('Parent node not found.')
    else:
        print('Adding: ', newNode, ppt, tag, canDo, newNodeParent)
        kbTree.add(newNode, ppt, tag, canDo, newNodeParent)


    print(kbTree.print_tree(kbTree.root, ''))
    print('-' * 20)


    # We can easily add if you know the parent(s)...
    # Now let's try inserting a node between existing nodes...~?
    # Simple insert between parent and child
    # Ex: rodent - hamsterX - hamster
    new_Node = 'rodentX'
    new_Parent = 'rodent'
    new_ppt = 'x'
    new_tag = 'XXX'
    new_canDo = 'x,y,z'
    
#    child_Node = 'hamster' # There may zero or many...
    
    # Does parnet class exist?
    parentNode = kbTree.find_node(kbTree.root, new_Parent)
    
    if parentNode == None:
        print('Parent node not found: ', parentNode)
    else:
        print('parentNode.key: ', parentNode.key)
        print('Existing children is/are:', parentNode.children)

        # Keep a copy of the parent children
        parentNodeChildren = [] 
        for c in parentNode.children:
            parentNodeChildren.append(c)

        print(len(parentNode.children))
        print(len(parentNodeChildren))

        print(parentNodeChildren)

        print('-' * 5)

        print('Adding/inserting new node: ', new_Node, new_ppt, new_tag, new_canDo, parentNode.key)
        kbTree.add(new_Node, new_ppt, new_tag, new_canDo, parentNode.key)

        insertedNode = kbTree.find_node(kbTree.root, new_Node)

        print('insertedNode.key: ', insertedNode.key)
        print('insertedNode.parentNode: ', insertedNode.parentNode)
        print('children mess:')
        print(insertedNode.children)
        print(len(insertedNode.children))
        print(type(insertedNode.children))
            
        for c in insertedNode.children:
            print(c)
                
        print('-' * 5)

        # Add the orignal parent children to inserted node
        for c in parentNodeChildren:
            insertedNode.children.append(c)


        print(insertedNode.children)
        print(len(insertedNode.children))
        print(type(insertedNode.children))
            
        for c in insertedNode.children:
            print(c)
                
        print('-' * 5)

        print(parentNode.children)

        # Keep the newly added child and clear the old children
        keepChild = parentNode.children[-1]
        parentNode.children.clear()
        parentNode.children.append(keepChild)

        print(parentNode.children)

#        for c in parentNode.children:
#            if c
#            print(c)

#        del parentNode.children[0] # I don't like just bindly removing [0]
        

        """

        if len(parent_node.children) == 1: # Assuming only "hamster"
            print('parent_node.children[0].key: ', parent_node.children[0].key)
            print('-' * 5)
            print('Adding/inserting new node: ', new_Node, new_ppt, new_tag, new_canDo, parent_node.key)
            kbTree.add(new_Node, new_ppt, new_tag, new_canDo, parent_node.key)
            insertedNode = kbTree.find_node(kbTree.root, new_Node)
            childNode  = kbTree.find_node(kbTree.root, child_Node)
            
            print('insertedNode.key: ', insertedNode.key)
            print('insertedNode.parentNode: ', insertedNode.parentNode)
            print('children mess:')
            print(insertedNode.children)
            print(len(insertedNode.children))
            print(type(insertedNode.children))
            
            for c in insertedNode.children:
                print(c)
                
            print('-' * 5)
            insertedNode.children.append(childNode) 
            print(insertedNode.children)
            print('insertedNode.children[0]: ', insertedNode.children[0])
            print(len(insertedNode.children))
            print(type(insertedNode.children))

            for c in insertedNode.children:
                print(c)


            print('-' * 5) # Now remove old child node from parent

            
            del parent_node.children[0] # only works for this example
            
        else:
            print('length greater then 1: ', len(parent_node.children))

        """


    

    # Modify canDo
    #
    """
    print('is going to learn how to fly...')
    node.canDo = 'fly'
    """
    """
    print('reset pookie...')
    node.canDo = 'see,eat,walk,run'

    canDo = kbTree.get_canDo(kbTree.root, testName)
    print(canDo)
    """
    """
    savePickle('kbTree', kbTree)
    """

    print('-' * 20)
    print(kbTree.print_tree(kbTree.root, ''))
    print('\n --- checkKB Complete ---')
