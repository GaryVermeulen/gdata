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
    print('---')

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
    print('-' * 10)


    # We can easily add if you know the parent(s)...
    # Now let's try inserting a node between existing nodes...~?
    # Simple insert between parent and child
    # Ex: rodent - hamsterX - hamster
    i_Node = 'hamsterX'
    i_Parent = 'rodent'
    i_ppt = 'x'
    i_tag = 'XXX'
    i_canDo = 'x,y,z'
    child_Node = 'hamster'
    
    # Does parnet class exist?
    p_node = kbTree.find_node(kbTree.root, i_Parent)
    
    if p_node == None:
        print('Parent node not found.')
    else:
        # Get the children of the parent class in order to
        childrenNodes = p_node.children
        print('p_node.key: ', p_node.key)
        print('Existing children is/are:', childrenNodes)
        for n in childrenNodes:
            print('n.key: ', n.key)
            if n.key == child_Node:
                print('Found the child of the parent to make child of new node...')
                print(n.key)
                n.parent = i_Node 
                print('Adding: ', i_Node, i_ppt, i_tag, i_canDo, i_Parent)
                kbTree.add(i_Node, i_ppt, i_tag, i_canDo, i_Parent)

                print('-' * 5)
                print(kbTree.print_tree(kbTree.root, ''))
                print('-' * 5)

                iNode = kbTree.find_node(kbTree.root, i_Node)
                print('iNode.key: ', iNode.key)
                print('iNode.parentNode: ', iNode.parentNode)
                print('iNode.children: ', iNode.children)
                

                orgChildNode = kbTree.find_node(kbTree.root, child_Node)
                print('orgChildNode.key: ', orgChildNode.key)
                print('orgChildNode.parentNode: ', orgChildNode.parentNode)
                print('orgChildNode.children: ', orgChildNode.children)

                for c in orgChildNode.children:
                    print(c)

                print('-' * 5)

                orgChildNode.parentNode = iNode.key

                print('orgChildNode.key: ', orgChildNode.key)
                print('orgChildNode.parentNode: ', orgChildNode.parentNode)
                print('orgChildNode.children: ', orgChildNode.children)
                
                print('-' * 5)


                orgCN = kbTree.find_node(kbTree.root, child_Node)
                print('orgCN.key: ', orgCN.key)
                print('orgCN.parentNode: ', orgCN.parentNode)
                print('orgCN.children: ', orgCN.children)
                
                
#                iNode.children = ''
#                iNode.children = [orgChildNode.parentNode]
#                print('new iNode.children: ', iNode.children)


    

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

    print('-' * 10)
    print(kbTree.print_tree(kbTree.root, ''))
    print('\n --- checkKB Complete ---')
