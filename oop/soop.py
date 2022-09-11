# soop.py
#
# Simple OOP in Python
#

class Dog:
    # Class attribute
    species = "Canis familiaris"
    
    # Instance attributes
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Instance method
#    def description(self):
#        return f"{self.name} is {self.age} years old."
    #
    def __str__(self):
        return f"{self.name} is {self.age} years old."


    # Another instance method
    def speak(self, sound):
        return f"{self.name} barks: {sound}"

#    pass
# End Class Dog

# Dog child classes...
#
class Terrier(Dog):
    def speak(self, sound="Arf"):
#        return f"{self.name} says {sound}"
        return super().speak(sound)
    
#    pass
# End Terrier child class

class Dachshund(Dog):
    pass

class Bulldog(Dog):
    pass

class GoldenRetriever(Dog):
    def speak(self, sound="Bark"):
#        return f"{self.name} says {sound}"
        return super().speak(sound)

# Differnet parent class...
#
class Car:
    def __init__(self, color, miles):
        self.color = color
        self.miles = miles

    def __str__(self):
        return f"The car {self.color} has {self.miles}."

    def __repr__(self):
#        return str(self)
        return f"I am a {self.color} with {self.miles}"
    
# End of Car parent class


## Yet another Parent class
##
class Counter:
    def __init__(self):
        self.current = 0

    def inc1(self):
        self.current += 1

    def dec1(self):
        self.current -= 1

    def val(self):
        return self.current

    def reset(self):
        self.current = 0
        
        
print ('END:soop.py')
