# Multiple Inheritance
Multiple inheritance is a type of inheritance wherein a child class inherits from more than one parent class:

`animal.py`
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def eat(self):
        print(f"{self.name} is eating.")
    
    def sleep(self):
        print(f"{self.name} is sleeping.")

class Prey(Animal):
    def flee(self):
        print(f"{self.name} is fleeing")

class Predator(Animal):
    def hunt(self):
        print(f"{self.name} is hunting")        
```

Let's say we have those classes and what we want to do is create a class that will inherite from `Prey` and `Predator`.

We will be doing a Fox class since it is both prey and predator and it will inherit the said classes and not only that it will also inherit the parent class of the two classes which is the `Animal`.

`main.py`
```python
class Fox(Prey, Predator):
    def play(self): # Foxes love to play LOL!
        print(f"{self.name} is playing") # as you can see even if the prey and the predator classes do not have the name attribute the Fox class is still able to use it

myFox = Fox("Ranger")

print(myFox.name)
myFox.hunt()
```

Now that is **easy**. What's difficult lies within the `init`. If the child class and the parent class has constructors. What's more difficult is when you child class has more than one parents with their own constructors and that is what the next lesson is. 