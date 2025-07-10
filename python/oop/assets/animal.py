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

