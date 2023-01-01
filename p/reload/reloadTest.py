# module reloading
#

import importlib
import myMod1

Cat = 'Cat'
Dog = 'Dog'
Bob = 'Bob'

mMod1 = myMod1.myFun1(Cat)

print('myMod1.myFun1(Cat) = ', mMod1)

x = input('Hit enter to contimue')
      
importlib.reload(myMod1)

mMod1 = myMod1.myFun1(Dog)

print('myMod1.myFun1(Dog) = ', mMod1)

x = input('Hit enter to contimue')
      
importlib.reload(myMod1)

mMod1 = myMod1.myFun1(Bob)

print('myMod1.myFun1(Bob) = ', mMod1)
