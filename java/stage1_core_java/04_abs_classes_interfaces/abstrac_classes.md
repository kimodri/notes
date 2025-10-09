# **Abstract Classes**

## **1. What is an Abstract Class?**

An **abstract class** is a special kind of class that cannot be instantiated (you cannot create objects directly from it).
It serves as a **blueprint** for other classes.

* It may contain **abstract methods** (methods without a body — meant to be implemented by subclasses).
* It can also contain **regular methods and fields** that subclasses can inherit or override.

## **2. Why Use Abstract Classes?**

* To provide **common structure and behavior** for all subclasses.
* To **force** subclasses to implement specific methods.
* To allow **shared fields and methods** across all subclasses.

## **3. Abstract Methods**

* Declared using the `abstract` keyword.
* Do **not** have a body (no `{ }`).
* Must be **implemented** by non-abstract subclasses.

Example:

```java
public abstract class Animal {
    public abstract void makeSound(); // Abstract method
}
```

## **4. Abstract Classes with Fields and Methods**

Abstract classes can still have:

* Fields (like `protected int speed;`)
* Constructors
* Concrete (non-abstract) methods

Example:

```java
// Vehicle.java
public abstract class Vehicle {
    protected float speed;

    public Vehicle(float speed) {
        this.speed = speed;
    }

    public abstract void start(); // Abstract method

    public void stop() {
        System.out.println("Vehicle stopped!");
    }
}
```

## **5. Implementing Abstract Methods**

When a class **extends** an abstract class, it must provide definitions for all abstract methods, or else it also becomes abstract.

```java
// ElectricCar.java
public class ElectricCar extends Vehicle {

    public ElectricCar(float speed) {
        super(speed); // Calls Vehicle's constructor
    }

    @Override
    public void start() {
        System.out.println("Electric Car is starting!");
    }
}
```

## **6. Using Abstract Classes in Code**

```java
// Main.java
public class Main {
    public static void main(String[] args) {
        // Vehicle v = new Vehicle(60); // ❌ Cannot instantiate abstract class
        Vehicle eCar = new ElectricCar(80); // ✅ Allowed

        eCar.start(); // Calls overridden method
        eCar.stop();  // Calls concrete method from Vehicle
    }
}
```

**Output:**

```
Electric Car is starting!
Vehicle stopped!
```

