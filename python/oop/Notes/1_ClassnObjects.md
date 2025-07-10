# Classes and Objects
This markdown note will focus on the creation of classes and their objects and other intricacies that revolve around them.

## Class Creation 

Much like java we can create a class:
```python
class Car:

    # This acts like a constructor:
    def __init__(self, model, year, color, is_for_sale):
        self.model = model
        self.year = year
        self.color = color
        self.is_for_sale = is_for_sale

        # I like to think of "self" in here as the same as the "this" of java

    def drive(self):
        print("Driving the {self.color} {self.model}")
```
## Importing a Class

You can put this class into another python file, so let's say you have two python files
- `car.py`
- `Main.py`

When you are in main, you can do:
```python
from car import Car

# Write your code
```

## Object Creation

Continuing on the above code you can create objects (instanced of the class) by:

```python
kimCar = Car("Mustang", 2025, "black", False)
audreyCar = Car("Corvette", 2023, white, True)
```

And let's say I want to print the attributes of my objects, I can do:
```python
print(kimCar.model)
print(audreyCar.model)

# and if I want to access my methods
kimCar.drive()
```

## Instanced and Class Variables

**Instance Variables**

Instance variables are variables that are specific to each instance of a class. They are defined within methods (usually the `__init__` method) using the `self` keyword, allowing each instance of the class to have its own copy of the variable.

**Class Variables**

Class variables are variables that are shared among all instances of a class. They are defined within the class but outside of any methods. All instances of the class share the same copy of a class variable.

**Ex:**

Let's say you have two Python files:
- `car.py`
- `main.py`

`car.py`

```python
class Car:
    wheels = 4  # Class variable
    number_of_cars = 0  # Class variable

    def __init__(self, model, year, color, convertible):
        self.model = model  # Instance variable
        self.year = year  # Instance variable
        self.color = color  # Instance variable
        self.convertible = convertible  # Instance variable
        # think of "self" as the name of the object
        Car.number_of_cars += 1  # Increment class variable for each new instance

    def drive(self):
        print(f"I am driving the {self.model}")

    def stop(self):
        print(f"I am stopping the {self.model}")
```
When you are in `Main`, you can do:
```python
from car import Car

# Create instances of the Car class
kimCar = Car("Mustang", 2025, "black", False)
audreyCar = Car("Corvette", 2023, "white", True)

# Access instance variables
print(kimCar.model)  # Output: Mustang
print(audreyCar.model)  # Output: Corvette

# Access class variables
print(Car.wheels)  # Output: 4
print(Car.number_of_cars)  # Output: 2

# Access instance methods
kimCar.drive()  # Output: I am driving the Mustang
audreyCar.stop()  # Output: I am stopping the Corvette
```

END