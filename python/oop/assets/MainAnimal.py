from animal import Animal, Dog, Cat, Mouse

# so we created objects here and let's try to access the attriutes and 
# methods they inherit
myDog = Dog("Scooby")
print(myDog.name)
print(myDog.is_alive)
myDog.walk()
myDog.eat()
myDog.talk()

myCat = Cat("Garfield")
print(myCat.name)
print(myCat.is_alive)
myCat.walk()
myCat.eat()
myCat.talk()


myMouse = Mouse("Mickey")
print(myMouse.name)
print(myMouse.is_alive)
myMouse.walk()
myMouse.eat()
myMouse.talk()



