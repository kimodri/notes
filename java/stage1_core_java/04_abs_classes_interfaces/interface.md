
# **Interfaces in Java**



## **1. What Is an Interface?**

An **interface** is a **blueprint for behavior**.
It tells a class *what* it must do, but not *how* to do it.

* Interfaces define **method signatures** (no implementation).
* They can also define **constants** (public static final variables).
* Classes that “agree” to follow an interface must **implement all its methods**.

Think of it as a **contract** — if a class implements it, it promises to provide the behavior described by the interface.



## **2. Declaring an Interface**

```java
public interface Drivable {
    void start();
    void stop();
}
```

Key points:

* Methods in an interface are **public and abstract** by default.
* No constructors — you can’t create an interface object directly.
* Fields are automatically **public static final** (constants).



## **3. Implementing an Interface**

A class uses the **`implements`** keyword to adopt an interface.

```java
public class ElectricCar implements Drivable {
    @Override
    public void start() {
        System.out.println("Electric Car is starting!");
    }

    @Override
    public void stop() {
        System.out.println("Electric Car is stopping!");
    }
}
```

* The `@Override` annotation ensures the method signatures match the interface.
* The class must implement **all** the interface methods (unless it’s abstract).



## **4. Interface Reference & Polymorphism**

You can use an interface type as a reference — this is **interface polymorphism**.

```java
Drivable d = new ElectricCar();
d.start();  // Prints: Electric Car is starting!
```

Even though `d` is declared as `Drivable`, it can refer to any class that implements `Drivable`.

**Why this matters:**
It lets you write flexible code — you can treat different classes uniformly if they share the same interface.


## **5. Implementing Multiple Interfaces**

A class can implement **more than one interface**, separated by commas.

```java
public interface Rechargeable {
    void chargeBattery();
}

public class ElectricCar implements Drivable, Rechargeable {
    @Override
    public void chargeBattery() {
        System.out.println("Electric Car is charging!");
    }
}
```
Java doesn’t allow multiple inheritance for classes,
but it allows **multiple interface implementation** — giving a class multiple “abilities”.


## **6. Default and Static Methods (Java 8+)**

Interfaces can have methods with bodies using the `default` and `static` keywords.

```java
public interface Flyable {
    void fly();

    default void land() {
        System.out.println("Landing safely...");
    }

    static void info() {
        System.out.println("All flyable things move through the air.");
    }
}
```

* `default` methods are inherited by implementing classes (they can override them).
* `static` methods belong to the interface itself and are called like `Flyable.info();`.


## **7. Key Takeaways**

| Concept             | Meaning                                       |
| :------------------ | :-------------------------------------------- |
| `interface`         | Defines a contract of behaviors               |
| `implements`        | A class agrees to fulfill that contract       |
| Multiple Interfaces | Gives a class multiple “roles” or “abilities” |
| Default Methods     | Let interfaces have optional implementations  |
| Interface Reference | Enables polymorphism across unrelated classes |


**Use interfaces when:**

* You want to define shared behavior across unrelated classes.
* You don’t need shared fields or constructors.
* You want flexibility — classes can implement multiple interfaces.
