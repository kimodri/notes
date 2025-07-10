# Inheritance in Python

- Inheritance allows a class to inherit attributes and methods from another class. 
- The class that inherits from another class is called the **child class** (or subclass)
- The class being inherited from is called the **parent class** (or superclass). 

## Basic Example of Inheritance

Let's explore the concept of inheritance through an example involving animals. We'll create a parent class `Animal` and several child classes (`Dog`, `Cat`, and `Mouse`) that inherit from the `Animal` class.

**`animal.py`**

```python
class Animal:
    def __init__(self, name):
        self.name = name
        self.is_alive = True
    
    def walk(self):
        print(f"{self.name} is walking! and it is {self.is_alive} that it is alive")
    
    def eat(self):
        print(f"{self.name} is eating and it is {self.is_alive} that it is alive")

# Now that if we want to have children classes:
class Dog(Animal):
    def talk(self):
        print(f"{self.name}: WOOF!")

class Cat(Animal):
    def talk(self):
        print(f"{self.name}: MEOW!")

class Mouse(Animal):
    def talk(self):
        print(f"{self.name}: SQUEEK!")
```

In the main.py file, you can create instances of the child classes and use their inherited and specific methods.

**`main.py`**

```python
from animal import Dog, Cat, Mouse

# Creating instances of child classes
myDog = Dog("Scooby")
print(myDog.name)        # Output: Scooby
print(myDog.is_alive)    # Output: True
myDog.walk()             # Output: Scooby is walking! and it is True that it is alive
myDog.eat()              # Output: Scooby is eating and it is True that it is alive
myDog.talk()             # Output: Scooby: WOOF!

myCat = Cat("Whiskers")
myCat.talk()             # Output: Whiskers: MEOW!

myMouse = Mouse("Jerry")
myMouse.talk()           # Output: Jerry: SQUEEK!
```

## Explanation 
- Parent Class (Animal): The Animal class defines common attributes (name and is_alive) and methods (walk and eat) that are shared by all animals.

- Child Classes (Dog, Cat, Mouse): These classes inherit from the Animal class and add their own specific method talk to provide different sounds for each animal type.

- Inheritance: The child classes (Dog, Cat, Mouse) inherit the attributes and methods (walk and eat) from the Animal class, promoting code reuse and reducing redundancy.

