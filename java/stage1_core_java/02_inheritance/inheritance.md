# **Inheritance in Java (with Sample Code)**

## **1. What is Inheritance**

* A **child class** can inherit **fields and methods** from a **parent class**.
* Purpose: **code reuse** and **polymorphism**.

**Sample Code:**

```java
class Animal {
    void eat() {
        System.out.println("Animal is eating");
    }
}

class Dog extends Animal {
    void bark() {
        System.out.println("Dog is barking");
    }
}

// Usage
Dog dog = new Dog();
dog.eat();  // inherited from Animal
dog.bark(); // own method
```


## **2. Syntax**

```java
class ChildClass extends ParentClass {
    // child class code
}
```

**Sample Code:**

```java
class Vehicle {
    void move() {
        System.out.println("Vehicle is moving");
    }
}

class Car extends Vehicle {
    void honk() {
        System.out.println("Car honks");
    }
}

Car myCar = new Car();
myCar.move(); // inherited
myCar.honk(); // own method
```


## **3. Fields and Methods (Access Modifiers)**

| Modifier  | Same Class | Same Package | Subclass | Everywhere |
| --------- | ---------- | ------------ | -------- | ---------- |
| private   | ✅          | ❌            | ❌        | ❌          |
| default   | ✅          | ✅            | ❌        | ❌          |
| protected | ✅          | ✅            | ✅        | ❌          |
| public    | ✅          | ✅            | ✅        | ✅          |

**Sample Code:**

```java
class Car {
    private int secretSpeed;
    protected int speed;
    public int maxSpeed;

    private void privateMethod() {}
    protected void protectedMethod() {}
    public void publicMethod() {}
}

class ElectricCar extends Car {
    void test() {
        // secretSpeed = 10; // ❌ cannot access
        speed = 50;          // ✅ accessible
        maxSpeed = 100;      // ✅ accessible
        // privateMethod();   // ❌ cannot access
        protectedMethod();   // ✅ accessible
        publicMethod();      // ✅ accessible
    }
}
```

## **4. Constructors in Inheritance**

* Parent constructor runs first.
* Use `super(...)` to call parent constructor.
* Private parent constructors **cannot** be called.

**Sample Code:**

```java
class Vehicle {
    protected float speed;

    protected Vehicle(float speed) {
        this.speed = speed;
    }
}

class Car extends Vehicle {
    private float fuel;

    public Car(float speed, float fuel) {
        super(speed); // calls Vehicle constructor
        this.fuel = fuel;
    }
}

Car myCar = new Car(50, 10);
```

## **5. Method Overriding**

* Subclass can provide its own version of a parent method.
* Use `@Override`.
* Optionally call `super.methodName()`.

**Sample Code:**

```java
class Vehicle {
    protected void start() {
        System.out.println("Vehicle starting");
    }
}

class ElectricCar extends Vehicle {
    @Override
    protected void start() {
        super.start(); // call parent
        System.out.println("Electric car starts silently");
    }
}

ElectricCar e = new ElectricCar();
e.start();
// Output:
// Vehicle starting
// Electric car starts silently
```


## **6. Polymorphism (Parent Reference → Child Object)**

* Reference type = parent
* Actual object = child
* Compiler checks **reference**
* Runtime uses **actual object**

**Sample Code:**

```java
Vehicle v = new Vehicle();
ElectricCar e = new ElectricCar();
Vehicle ref = new ElectricCar(); // parent reference, child object

v.start();    // Vehicle starting
e.start();    // Electric car starts silently
ref.start();  // Electric car starts silently
```



## **7. Complete Example: Vehicle + ElectricCar**

```java
// Vehicle.java
public class Vehicle {
    protected float speed;
    private float fuel;

    public Vehicle(float speed, float fuel) {
        this.speed = speed;
        this.fuel = fuel;
    }

    protected void start() {
        System.out.println("Vehicle is starting!");
    }

    public void refuel(float amount) {
        this.fuel += amount;
    }
}

// ElectricCar.java
public class ElectricCar extends Vehicle {
    private float batteryLevel;

    public ElectricCar(float speed, float fuel, float batteryLevel) {
        super(speed, fuel);
        this.batteryLevel = batteryLevel;
    }

    @Override
    public void start() {
        super.start();
        System.out.println("Electric car starts silently!");
    }

    public void chargeBattery(float amount) {
        this.batteryLevel += amount;
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Vehicle v = new Vehicle(1, 1);
        ElectricCar e = new ElectricCar(1, 1, 1);
        Vehicle ref = new ElectricCar(2, 2, 2);

        v.start();    // Vehicle is starting!
        e.start();    // Vehicle is starting!
                      // Electric car starts silently!
        ref.start();  // Vehicle is starting!
                      // Electric car starts silently!
    }
}
```

**Key Takeaways**

1. Use **protected** for fields/methods meant for inheritance.
2. Always call parent constructor via `super(...)`.
3. **Private parent constructors** prevent inheritance.
4. Overriding + polymorphism allows **dynamic behavior at runtime**.
5. Access modifiers control **visibility and extendability**.
