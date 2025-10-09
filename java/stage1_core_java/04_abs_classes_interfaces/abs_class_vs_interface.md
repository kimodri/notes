# **Abstract Classes vs Interfaces in Java**


## **1. Core Idea**

Both **abstract classes** and **interfaces** define common behaviors that other classes can share — but they serve different purposes.

| Feature          | Abstract Class                                           | Interface                                                                    |
| :--------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------- |
| Purpose          | Provides a **base class** with shared state and behavior | Defines a **contract** of methods that must be implemented                   |
| Fields           | Can have **instance variables**                          | Can only have **constants** (`public static final`)                          |
| Methods          | Can have **abstract** and **concrete** methods           | Mostly **abstract** methods, but can include **default** and **static** ones |
| Constructors     | Can have constructors (called via `super()`)             | Cannot have constructors                                                     |
| Inheritance      | A class can **extend only one** abstract class           | A class can **implement multiple** interfaces                                |
| Access Modifiers | Can have `protected` or `private` members                | All members are implicitly `public`                                          |

---

## **2. When to Use Each**

### **Use an Abstract Class when:**

* You want to **share fields or base behavior** among subclasses.
* There’s a clear **“is-a” relationship** between parent and child.
* You expect to have **common code** that subclasses can reuse.

Example:

```java
public abstract class Vehicle {
    protected float speed;

    public Vehicle(float speed) {
        this.speed = speed;
    }

    public abstract void start();
}
```

```java
public class Car extends Vehicle {
    public Car(float speed) {
        super(speed);
    }

    @Override
    public void start() {
        System.out.println("Car is starting!");
    }
}
```

---

### **Use an Interface when:**

* You want to define **behavioral contracts** without worrying about implementation details.
* You want **unrelated classes** to share common behavior.
* You need **multiple inheritance of behavior**, which Java supports through interfaces.

Example:

```java
public interface Drivable {
    void drive();
}

public interface Rechargeable {
    void recharge();
}

public class ElectricCar implements Drivable, Rechargeable {
    @Override
    public void drive() {
        System.out.println("Electric car is driving.");
    }

    @Override
    public void recharge() {
        System.out.println("Electric car is recharging.");
    }
}
```

Here, `ElectricCar` gains the abilities of both **Drivable** and **Rechargeable**, which is something not possible with classes alone.

---

## **3. Why Interfaces Enable “Multiple Inheritance of Type”**

Java does not allow a class to extend more than one superclass:

```java
// Invalid in Java
public class Drone extends Machine, Flyable { ... }
```

This restriction avoids ambiguity (such as the “diamond problem” in other languages).

However, **interfaces solve this** by allowing a class to implement multiple interfaces:

```java
public interface Machine {
    void operate();
}

public interface Flyable {
    void fly();
}

public class Drone implements Machine, Flyable {
    @Override
    public void operate() {
        System.out.println("Drone operating.");
    }

    @Override
    public void fly() {
        System.out.println("Drone flying.");
    }
}
```

In this case:

* `Drone` inherits *no state* (since interfaces have no fields),
* but it adopts the *behavioral contracts* of both `Machine` and `Flyable`.

This is Java’s safe form of **multiple inheritance**, achieved through **interfaces**, not classes.

---

## **4. Summary**

| Aspect                       | Abstract Class   | Interface                 |
| :--------------------------- | :--------------- | :------------------------ |
| Can have fields              | Yes              | No (only constants)       |
| Can have constructors        | Yes              | No                        |
| Can have implemented methods | Yes              | Yes (`default`, `static`) |
| Inherits using               | `extends`        | `implements`              |
| Multiple inheritance         | No               | Yes                       |
| Purpose                      | Shared base code | Shared behavior contract  |


**In short:**

* Use **abstract classes** when you want subclasses to share common state or behavior.
* Use **interfaces** when you want to define a set of capabilities that can be added to any class — especially when you need multiple inheritance of type.
